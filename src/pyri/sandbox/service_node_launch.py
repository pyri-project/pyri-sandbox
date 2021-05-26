from pyri.plugins.service_node_launch import ServiceNodeLaunch, PyriServiceNodeLaunchFactory


launches = [
    ServiceNodeLaunch("sandbox", "pyri.sandbox", "pyri.sandbox",default_devices=[("pyri_sandbox","sandbox")])
]

class SandboxLaunchFactory(PyriServiceNodeLaunchFactory):
    def get_plugin_name(self):
        return "pyri.sandbox"

    def get_service_node_launch_names(self):
        return ["sandbox"]

    def get_service_node_launches(self):
        return launches

def get_service_node_launch_factory():
    return SandboxLaunchFactory()

        
