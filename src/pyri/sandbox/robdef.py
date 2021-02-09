from typing import List
from RobotRaconteurCompanion.Util import RobDef as robdef_util
from pyri.plugins.robdef import PyriRobDefPluginFactory

class SandboxRobDefPluginFactory(PyriRobDefPluginFactory):
    def __init__(self):
        super().__init__()

    def get_plugin_name(self):
        return "pyri-sandbox"

    def get_robdef_names(self) -> List[str]:
        return ["tech.pyri.sandbox"]

    def  get_robdefs(self) -> List[str]:
        return get_sandbox_robdef()

def get_robdef_factory():
    return SandboxRobDefPluginFactory()

def get_sandbox_robdef():
    return robdef_util.get_service_types_from_resources(__package__,["tech.pyri.sandbox"])