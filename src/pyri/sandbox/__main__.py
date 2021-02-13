import sys
import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
from .pyri_sandbox import PyriSandbox
import argparse
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil
from pyri.plugins import robdef as robdef_plugins
import appdirs
from pathlib import Path
import subprocess
from importlib import resources

def main():

    if "--install-blockly-compiler" in sys.argv:        
        install_blockly_compiler()
        exit(0)

    parser = argparse.ArgumentParser(description="PyRI Variable Storage Service Node")    
    parser.add_argument("--device-info-file", type=argparse.FileType('r'),default=None,required=True,help="Device info file for sandbox service (required)")
    parser.add_argument('--device-manager-url', type=str, default=None,required=True,help="Robot Raconteur URL for device manager service (required)")
    parser.add_argument("--wait-signal",action='store_const',const=True,default=False, help="wait for SIGTERM or SIGINT (Linux only)")
    parser.add_argument("--install-blockly-compiler", action="store_true",default=False,help="Install the Blockly compiler for current user")
    
    args, _ = parser.parse_known_args()

    RRC.RegisterStdRobDefServiceTypes(RRN)
    robdef_plugins.register_all_plugin_robdefs(RRN)

    with args.device_info_file:
        device_info_text = args.device_info_file.read()

    info_loader = InfoFileLoader(RRN)
    device_info, device_ident_fd = info_loader.LoadInfoFileFromString(device_info_text, "com.robotraconteur.device.DeviceInfo", "device")

    attributes_util = AttributesUtil(RRN)
    device_attributes = attributes_util.GetDefaultServiceAttributesFromDeviceInfo(device_info)

    with RR.ServerNodeSetup("tech.pyri.sandbox",59903,argv=sys.argv):

        dev_manager = PyriSandbox(args.device_manager_url, device_info=device_info, node = RRN) 

        service_ctx = RRN.RegisterService("sandbox","tech.pyri.sandbox.PyriSandbox",dev_manager)
        service_ctx.SetServiceAttributes(device_attributes)

        if args.wait_signal:  
            #Wait for shutdown signal if running in service mode          
            print("Press Ctrl-C to quit...")
            import signal
            signal.sigwait([signal.SIGTERM,signal.SIGINT])
        else:
            #Wait for the user to shutdown the service
            if (sys.version_info > (3, 0)):
                input("Server started, press enter to quit...")
            else:
                raw_input("Server started, press enter to quit...")

        dev_manager.close()

def install_blockly_compiler():
    print("Installing blockly compiler...")

    compiler_dir = Path(appdirs.user_data_dir(appname="pyri-sandbox", appauthor="pyri-project", roaming=False))
    
    compiler_dir = compiler_dir.joinpath("blockly_compiler")
    print(f"Installing compiler to: {compiler_dir}")
    compiler_dir.mkdir(exist_ok=True,parents=True)
    subprocess.check_call("npm install node-blockly",cwd=str(compiler_dir),shell=True)

    compile_script = resources.read_text(__package__,"compile_blockly.js")

    with open(compiler_dir.joinpath("compile_blockly.js"),"w") as f:
        f.write(compile_script)

    print("Done!")


if __name__ == "__main__":
    sys.exit(main() or 0)
