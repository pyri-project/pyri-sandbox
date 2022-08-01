import sys
import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
from .pyri_sandbox import PyriSandbox
import argparse
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil
from pathlib import Path
from importlib import resources
from pyri.util.service_setup import PyriServiceNodeSetup
import os

def main():

    parser = argparse.ArgumentParser(description="PyRI Procedure Sandbox Service Node")    
    parser.add_argument("--blockly-compiler-dir",type=str,default=None,help="Directory containing blockly compiler NodeJS files")
    
    with PyriServiceNodeSetup("tech.pyri.sandbox",59903,argv=sys.argv, \
        default_info = (__package__,"pyri_sandbox_default_info.yml"), \
        arg_parser = parser, register_plugin_robdef=True,
        distribution_name="pyri-sandbox") as service_node_setup:

        args = service_node_setup.argparse_results

        blockly_compiler_dir = None
        if args.blockly_compiler_dir is not None:
            blockly_compiler_dir = args.blockly_compiler_dir
        elif "PYRI_SANDBOX_BLOCKLY_COMPILER_DIR" in os.environ:
            blockly_compiler_dir = os.environ["PYRI_SANDBOX_BLOCKLY_COMPILER_DIR"]

        sandbox = PyriSandbox(service_node_setup.device_manager, device_info=service_node_setup.device_info_struct, \
             node = RRN, blockly_compiler_dir = blockly_compiler_dir)

        service_node_setup.register_service("sandbox","tech.pyri.sandbox.PyriSandbox",sandbox)

        service_node_setup.wait_exit()

        sandbox._close()

if __name__ == "__main__":
    sys.exit(main() or 0)
