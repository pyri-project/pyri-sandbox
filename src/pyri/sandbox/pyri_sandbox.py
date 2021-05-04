

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
import sys

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
        self.printed.append(str(text))


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

        self._executors = []
        self._stopped = False
        self._running = False

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
        executor = ExecuteProcedureGenerator(self, procedure_name, byte_code, sandbox_builtins, sandbox_globals, loc, params, print_collector, self._node, self._device_manager, self._status_type)
        with self._lock:
            if self._stopped:
                raise RR.InvalidOperationException("Sandbox is stopping")
            self._executors.append(executor)
        return executor

    def stop_all(self):
        with self._lock:
            self._stopped = True
            ex = self._executors
        for e in ex:
            e._stopped()

    def _close(self):
        try:
            self._blockly_compiler.close()
        except:
            pass

    def _execution_complete(self, executor):
        with self._lock:
            if executor in self._executors:
                self._executors.remove(executor)
                self._stopped = False
                self._running = False
class PyriSandboxStoppedError(BaseException):
    pass

class ExecuteProcedureGenerator:

    def __init__(self, parent, procedure_name, byte_code, builtins, sandbox_globals,loc, params, print_collector, node, device_manager, status_type):
        self._parent = parent
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
        self._is_stopped = False

    def Next(self):
        with self._parent._lock:
            if self._run:
                raise StopIterationException("Procedure completed")
            self._run = True
        
        if self._is_stopped:
            raise RR.OperationAbortedException("Procedure has been stopped")

        old_trace = sys.gettrace()        
        with self._parent._lock:
            if self._parent._running:
                raise RR.InvalidOperationException("Sandbox already running a procedure")
            self._parent._running = True
        try:
                     
            with PyriSandboxContextScope(self._node, self._device_manager, self._print_collector.write, self._action_runner):
                sys.settrace(self._pyri_sandbox_trace)
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
        except PyriSandboxStoppedError:
            raise RR.OperationAbortedException("Procedure has been stopped")
        finally:
            sys.settrace(old_trace)
            self._parent._execution_complete(self)

    def Close(self):
        self._do_abort()

    def Abort(self):
        self._do_abort()

    def _stopped(self):
        self._do_abort()

    def _do_abort(self):
        with self._parent._lock:
            if not self._run:
                self._run = True
                self._parent._execution_complete(self)
                return            
        self._action_runner.abort()
        self._is_stopped = True

    def _pyri_sandbox_trace(self, frame, event, arg):
        if self._is_stopped:
            raise PyriSandboxStoppedError()


       

        