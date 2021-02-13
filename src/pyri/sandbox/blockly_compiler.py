
import subprocess
import tempfile
import os.path as path
import urllib.request
from urllib.parse import quote
import re
from pathlib import Path
import appdirs

compiler_node_script = Path(appdirs.user_data_dir(appname="pyri-sandbox", appauthor="pyri-project", roaming=False)).joinpath("blockly_compiler").joinpath("compile_blockly.js")

class BlocklyCompiler:
    def __init__(self):
        self._p = subprocess.Popen(["node",compiler_node_script],stdout=subprocess.PIPE)
        init_line = self._p.stdout.readline().decode('utf8')
        init_line_match = re.match("^ready;(\d+)$", init_line.strip())
        assert init_line_match is not None, "Could not start Blockly compiler. Run 'pyri-sandbox-service --install-blockly-compiler'"
        port = int(init_line_match.group(1))
        self._p_addr = f'http://127.0.0.1:{port}'
        pass

    def _call_p(self, arg):
        print("Begin req")
        res = urllib.request.urlopen(f"{self._p_addr}?command=compile&arg={quote(arg)}")
        res_line = res.read()
        res.close()
        print("End req")
        if res_line.decode('utf8').strip() != "done":
            #TODO: include error message
            raise Exception(f"Blockly compile error: {res_line.decode('utf8').strip()}")

    def compile(self, procedure_name, procedure_src):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(path.join(tmpdir,"blockly_src.xml"),"w") as f_out:
                f_out.write(procedure_src)

            self._call_p(tmpdir)

            with open(path.join(tmpdir,"blockly_src_compiled.py"),"r") as f_in:
                c = f_in.read()

            return c

    def close(self):
        try:
            self._p.terminate()
        except:
            pass