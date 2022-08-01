import subprocess
import argparse
import tempfile
from pathlib import Path
import shutil

def get_blockly_compiler_install_dir():
    current_dir = Path(__file__).parent
    return (current_dir / ".." / ".." / "src" / "pyri" / "sandbox").resolve()

def build_packed_compiler(outdir):
    with tempfile.TemporaryDirectory() as dir1:
        dir2 = Path(dir1)
        subprocess.check_call(f"npm run build_blockly_compiler -- -o {dir2}", shell=True)
        shutil.copy((dir2 / "index.js"), Path(outdir) / "blockly_compile.js")

def main():
    parser = argparse.ArgumentParser(description='Build and install the combined blockly_compile.js script')
    parser.add_argument('--outdir',type=str,default=None,help="Directory to save blockly_compile.js. Defaults to Python package location")

    args = parser.parse_args()

    outdir = get_blockly_compiler_install_dir()
    if args.outdir is not None:
        outdir = args.outdir
    
    build_packed_compiler(outdir)

if __name__ == "__main__":
    main()