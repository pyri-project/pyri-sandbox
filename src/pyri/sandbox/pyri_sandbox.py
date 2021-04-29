

import re
from RestrictedPython import compile_restricted
import threading
import RobotRaconteur as RR
from RobotRaconteur.RobotRaconteurPythonError import StopIterationException
from pyri.device_manager_client import DeviceManagerClient
from .restricting_transformer import PyriRestrictingNodeTransformer
from .blockly_compiler import BlocklyCompiler
from . import guards
from pyri.sandbox_context import PyriSandboxContext, PyriSandboxContextScope, PyriSandboxActionRunner
from pyri.plugins.sandbox_functions import get_all_plugin_sandbox_functions
from pyri.plugins.blockly import get_all_blockly_blocks

import copy

_valid_name_re = re.compile('[a-zA-Z][a-zA-Z0-9_]*')
_policy = PyriRestrictingNodeTransformer

#safe_builtins = copy.deepcopy(safe_builtins_zope)



class PrintCollector:
    def __init__(self):
        self.printed = []
    
    def __call__(self, _gettattr_=None):
        return self

    def write(self, text):
        self.printed.append(text)

    def _call_print(self, text):
        self.printed.append(text)


class PyriSandbox():

    def __init__(self, device_manager_url, device_info = None, node : RR.RobotRaconteurNode = None):
        self._lock = threading.RLock()
        if node is None:
            self._node = RR.RobotRaconteurNode.s
        else:
            self._node = node
        self.device_info = device_info

        self._status_type = self._node.GetStructureType('tech.pyri.sandbox.ProcedureExecutionStatus')
        self._action_const = self._node.GetConstants('com.robotraconteur.action')

        self._blockly_compiler = BlocklyCompiler()

        self._device_manager = DeviceManagerClient(device_manager_url)
        self._device_manager.refresh_devices(1)

    def execute_procedure(self, procedure_name, params):
        
        if _valid_name_re.match(procedure_name) is None:
            raise RR.InvalidArgumentException("Procedure name is invalid")
        
        variable_manager = self._device_manager.get_device_client("variable_storage",1)

        procedure_src = variable_manager.getf_variable_value("procedure",procedure_name)
        procedure_tags = variable_manager.getf_variable_tags("procedure",procedure_name)

        assert isinstance(procedure_src.data,str), "Procedure variable must be string"

        if "pyri" in procedure_tags:
            pyri_src = procedure_src.data
        elif "blockly" in procedure_tags:
            blockly_blocks = get_all_blockly_blocks()
            pyri_src = self._blockly_compiler.compile(procedure_name, procedure_src.data, blockly_blocks)
        else:
            assert False, "Invalid procedure type (must be pyri or blockly)"
        
        plugin_sandbox_functions = get_all_plugin_sandbox_functions()

        loc = {}
        
        byte_code = compile_restricted(pyri_src, '<pyri_sandbox>', 'exec',  policy = _policy)
        sandbox_builtins = guards.get_pyri_builtins_with_name_guard(plugin_sandbox_functions.keys())
        sandbox_globals = {'__builtins__': sandbox_builtins}
        sandbox_globals.update(plugin_sandbox_functions)
        print_collector = PrintCollector()
        sandbox_globals["_print_"] =print_collector

        return ExecuteProcedureGenerator(procedure_name, byte_code, sandbox_builtins, sandbox_globals, loc, params, print_collector, self._node, self._device_manager, self._status_type)

    def _close(self):
        try:
            self._blockly_compiler.close()
        except:
            pass

class ExecuteProcedureGenerator:

    def __init__(self, procedure_name, byte_code, builtins, sandbox_globals,loc, params, print_collector, node, device_manager, status_type):
        self._procedure_name = procedure_name
        self._byte_code = byte_code
        self._bultins = builtins
        self._globals = sandbox_globals
        self._loc = loc
        self._params = params
        self._status_type = status_type
        self._print_collector = print_collector
        self._node = node
        self._device_manager = device_manager
        self._run = False
        self._action_runner = PyriSandboxActionRunner()

    def Next(self):
        if self._run:
            raise StopIterationException("Procedure completed")

        self._run = True
        with PyriSandboxContextScope(self._node, self._device_manager, self._print_collector.write, self._action_runner):
            #TODO: Execute in different thread
            exec(self._byte_code, self._globals, self._loc)
            if self._params is None:
                res = self._loc[self._procedure_name]()
            else:
                res = self._loc[self._procedure_name](*self._params)

            assert isinstance(res,str) or res is None, "Result of procedure must be string"

            ret = self._status_type()
            # TODO: use constants
            ret.action_status = 3
            ret.printed = self._print_collector.printed
            ret.result_code = res or "SUCCESS"

            return ret

    def Close(self):
        pass

    def Abort(self):
        pass

        

        