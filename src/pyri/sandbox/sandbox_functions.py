from pyri.plugins.sandbox_functions import PyriSandboxFunctionsPluginFactory

import time

def sleep(t):
    time.sleep(t)


class SandboxFunctionsPluginFactory(PyriSandboxFunctionsPluginFactory):
    def get_plugin_name(self):
        return "pyri-sandbox"

    def get_sandbox_function_names(self):
        return [] #["sleep"]

    def get_sandbox_functions(self):
        return {} #{"sleep": sleep}


def get_sandbox_functions_factory():
    return SandboxFunctionsPluginFactory()