import subprocess
import tempfile
import os.path as path

node_script = r"C:\Users\wasonj\Documents\pyri\experiments\blockly_nodejs_compile\compile_blockly.js"

class BlocklyCompiler:
    def __init__(self):
        pass
    def compile(self, procedure_name, procedure_src):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(path.join(tmpdir,"blockly_src.xml"),"w") as f_out:
                f_out.write(procedure_src)

            subprocess.check_call(["node", node_script, tmpdir])

            with open(path.join(tmpdir,"blockly_src_compiled.py"),"r") as f_in:
                c = f_in.read()

            return c