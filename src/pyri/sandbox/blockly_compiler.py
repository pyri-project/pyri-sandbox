
import subprocess
import tempfile
import os.path as path
import urllib.request
from urllib.parse import quote
import re
from pathlib import Path
import argparse
import json
import importlib_resources
import sys
import os
import struct
import threading
import time
import traceback
from pyri.plugins.blockly import blockly_block_to_json

if sys.platform == "win32":
    import msvcrt

class BlocklyCompiler:    
    def __init__(self,compiler_dir = None):
        self._p_lock = threading.Lock()
        with importlib_resources.path(__package__,"blockly_compile.js") as p:
            compiler_node_script_default = p
        if compiler_dir is None:
            compiler_node_script = compiler_node_script_default
        else:
            compiler_node_script = Path(compiler_dir).joinpath("blockly_compile.js")
        self._p = subprocess.Popen(["node",compiler_node_script],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        if sys.platform == "win32":
            msvcrt.setmode(self._p.stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(self._p.stdout.fileno(), os.O_BINARY)
        self._p_keepalive_timer_lock = threading.Lock()
        self._p_keepalive_timer_keep_going = True
        self._p_keepalive_timer_interval = 15
        with self._p_keepalive_timer_lock:
            self._p_keepalive_timer = threading.Timer(interval=self._p_keepalive_timer_interval, function=self._p_keepalive)
            self._p_keepalive_timer.start()
            self._p_last_keepalive = time.time()

    def _call_p(self, send_msg):        
        self._p_last_keepalive = time.time()
        send_msg_json = json.dumps(send_msg).encode("utf-8")
        send_msg_json_len = struct.pack("<I",len(send_msg_json))
        self._p.stdin.write(send_msg_json_len + send_msg_json)
        self._p.stdin.flush()
        recv_msg_json_len_b = self._p.stdout.read(4)
        recv_msg_json_len = struct.unpack("<I", recv_msg_json_len_b)[0]
        recv_msg_json = self._p.stdout.read(recv_msg_json_len)
        recv_msg = json.loads(recv_msg_json)
        
        if recv_msg["return"] == "error":
            err_stack = recv_msg.get("stack","<unknown>")
            raise Exception(f"Blockly compile error: {err_stack}")
        return recv_msg

    def _p_keepalive(self):
        with self._p_keepalive_timer_lock:
            self._p_keepalive_timer = None
        try:
            if time.time() - self._p_last_keepalive > self._p_keepalive_timer_interval-0.5:
                locked = self._p_lock.acquire(blocking=False)
                if locked:
                    try:
                        self._call_p({"command": "keepalive"})
                    except:
                        traceback.print_exc()
                    finally:
                        self._p_lock.release()
        finally:
            with self._p_keepalive_timer_lock:
                if  self._p_keepalive_timer_keep_going:
                    self._p_keepalive_timer = threading.Timer(interval=self._p_keepalive_timer_interval, function=self._p_keepalive)
                    self._p_keepalive_timer.start()

    def compile(self, procedure_name, procedure_src, blockly_blocks):

        arg = get_compile_request_args(procedure_name, procedure_src, blockly_blocks)
        send_msg = {"command": "compile", "arg": arg}
        with self._p_lock:
            recv_msg = self._call_p(send_msg)
        if recv_msg["return"] != "done":
            raise Exception(f"Blockly compilation failed for procedure {procedure_name}")
        return recv_msg["py_src"]        

    def close(self):
        try:
            with self._p_keepalive_timer_lock:
                self._p_keepalive_timer_keep_going = False
                self._p_keepalive_timer.cancel()
                self._p_keepalive_timer = None
        except:
            pass
        
        _p = self._call_p
        self._call_p = None

        try:
            locked = self._p_lock.acquire(blocking=True,timeout=2)
            if locked:
                try:
                    _p({"command": "quit"})
                finally:
                    self._p_lock.release()
        except:
            pass
        try:
            _p.wait(1)
            return
        except:
            pass
        try:
            _p.terminate()
        except:
            pass

def get_compile_request_args(procedure_name, procedure_src, blockly_blocks):

    blockly_blocks_list = [blockly_block_to_json(b) for b in blockly_blocks.values()]

    if (isinstance(procedure_src,str)):
        procedure_src = json.loads(procedure_src)

    return {
        "name": procedure_name,
        "blockly_json_src": procedure_src,
        "blockly_blocks": blockly_blocks_list
    }

def compile_blockly_file(file, output=None, arg_file=None):
    json_src = file.read()
    json_dict = json.loads(json_src)
    blocks1 = json_dict["blocks"]["blocks"]
    assert len(blocks1) == 1, "Expect one procedures_defnoreturn top level block for procedure"
    block2 = blocks1[0]
    assert block2["type"] == "procedures_defnoreturn", "Expect one procedures_defnoreturn top level block for procedure"
    procedure_name = block2["fields"]["NAME"]
    
    from pyri.plugins.blockly import get_all_blockly_blocks
    blockly_blocks = get_all_blockly_blocks()

    if arg_file is not None:
        args_json = get_compile_request_args(procedure_name, json_src, blockly_blocks)
        json.dump(args_json, arg_file)
        return
    compiler_dir = os.environ.get("PYRI_SANDBOX_BLOCKLY_COMPILER_DIR",None)
    compiler = BlocklyCompiler(compiler_dir)
    try:
        py_src = compiler.compile(procedure_name, json_src, blockly_blocks)
    finally:
        try:
            compiler.close()
        except:
            pass

    if output is not None:
        output.write(py_src)
    else:
        print(py_src)

def main():

    parser = argparse.ArgumentParser(description='Compile a Blockly JSON file to Python')
    parser.add_argument('--arg-file',type=argparse.FileType('w'),default=None,help="Output compiler argument to file")
    parser.add_argument('--output',type=argparse.FileType('w'),default=None,help="Output filename")
    parser.add_argument('file', type=argparse.FileType('r'), help="Blockly JSON file to compile")

    args = parser.parse_args()

    compile_blockly_file(args.file,args.output,args.arg_file)
    

if __name__ == "__main__":
    main()
