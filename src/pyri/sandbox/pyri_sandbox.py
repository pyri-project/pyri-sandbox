

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
import traceback
import time

from RobotRaconteurCompanion.Util.DateTimeUtil import DateTimeUtil

_valid_name_re = re.compile('[a-zA-Z][a-zA-Z0-9_]*')
_policy = PyriRestrictingNodeTransformer

#safe_builtins = copy.deepcopy(safe_builtins_zope)



class PrintCollector:
    def __init__(self):
        self.printed = []
        self.print_event = RR.EventHook()
    
    def __call__(self, _gettattr_=None):
        return self

    def write(self, text):
        self.printed.append(str(text))
        self.print_event.fire(str(text))

    def _call_print(self, text):
        self.printed.append(str(text))
        self.print_event.fire(str(text))


class PyriSandbox():

    def __init__(self, device_manager_url, device_info = None, node : RR.RobotRaconteurNode = None, blockly_compiler_dir = None):
        self._lock = threading.RLock()
        if node is None:
            self._node = RR.RobotRaconteurNode.s
        else:
            self._node = node
        self.device_info = device_info
        self._blockly_compiler_dir = blockly_compiler_dir

        self._status_type = self._node.GetStructureType('tech.pyri.sandbox.ProcedureExecutionStatus')
        self._action_const = self._node.GetConstants('com.robotraconteur.action')
        self._sandbox_const = self._node.GetConstants('tech.pyri.sandbox')
        self._output_codes = self._sandbox_const["ProcedureOutputTypeCode"]
        
        self._blockly_compiler = BlocklyCompiler(compiler_dir=self._blockly_compiler_dir)

        self._device_manager = DeviceManagerClient(device_manager_url)
        self._device_manager.refresh_devices(1)

        self._executors = []
        self._stopped = False
        self._running = False

        self._output = []
        self._output_evt = threading.Condition()

        self._datetime_util = DateTimeUtil(node = self._node)
        self._run_number = 0

        self._procedure_output_type = self._node.GetStructureType('tech.pyri.sandbox.ProcedureOutput')
        self._procedure_output_list_type = self._node.GetStructureType('tech.pyri.sandbox.ProcedureOutputList')


    def execute_procedure(self, procedure_name, params):
        try:
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

            def send_local_print(text):
                self._send_print(text, procedure_name, self._output_codes["output"])
            print_collector = PrintCollector()
            print_collector.print_event += send_local_print
            sandbox_globals["_print_"] =print_collector
            self._run_number += 1
            run_number = self._run_number
            executor = ExecuteProcedureGenerator(self, procedure_name, byte_code, sandbox_builtins, sandbox_globals, loc, params, print_collector, self._node, self._device_manager, self._status_type, run_number)
            with self._lock:                
                if self._stopped:
                    raise RR.InvalidOperationException("Sandbox is stopping")
                self._executors.append(executor)
            self._send_print(f"Procedure \"{procedure_name}\" started", procedure_name, self._output_codes["status"])
            return executor
        except Exception:
            self._send_print(f"Execute procedure \"{procedure_name}\" failed:\n\n{traceback.format_exc()}", procedure_name, self._output_codes["error"])
            raise

    def stop_all(self):
        with self._lock:            
            ex = self._executors
            if len(ex) != 0:
                self._stopped = True

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


    def _send_print(self, text, procedure_name, status):
        with self._output_evt:
            o = self._procedure_output_type()
            o.output_number = 1
            if len(self._output) > 0:
                o.output_number = self._output[-1].output_number + 1
            o.output_type = status
            o.time = self._datetime_util.UtcNow(self.device_info)
            o.procedure_name = procedure_name
            o.procedure_run_number = 0
            o.output = text

            self._output.append(o)
            while len(self._output) > 10000:
                self._output.pop(0)

            self._output_evt.notify_all()

    def getf_output(self):
        return PyriSandboxOutputGenerator(self)

class PyriSandboxOutputGenerator:
    def __init__(self,parent):
        self.parent = parent
        self._current_num = -1
        self._max_output = 1000
        self._lock = threading.Lock()
        self._closed = False
        self._node = self.parent._node
        self._procedure_output_type = self._node.GetStructureType('tech.pyri.sandbox.ProcedureOutput')
        self._procedure_output_list_type = self._node.GetStructureType('tech.pyri.sandbox.ProcedureOutputList')


    def Next(self):
        with self.parent._output_evt:

            t1 = time.time()
            while time.time() - t1 < 10.0:
                if self._closed:
                    raise RR.StopIterationException("")

                if (len(self.parent._output) == 0):
                    self._current_num = 0

                if len(self.parent._output) > 0 and self._current_num < self.parent._output[-1].output_number:
                    if self._current_num < 0:
                        self._current_num = self.parent._output[-1].output_number
                        continue
                    start_ind = 0
                    if self._current_num+1 > self.parent._output[0].output_number:
                        start_ind = self._current_num + 1 - self.parent._output[0].output_number

                    end_ind = start_ind + self._max_output
                    if end_ind > len(self.parent._output):
                        end_ind = len(self.parent._output)
                    if end_ind != start_ind:
                        ret = self._procedure_output_list_type()
                        ret.first_output_number = self.parent._output[start_ind].output_number
                        ret.output_list = []
                        for i in range(start_ind,end_ind):
                            ret.output_list.append(self.parent._output[i])
                            self._current_num = ret.output_list[-1].output_number
                        
                        return ret

                self.parent._output_evt.wait(10.0 - (time.time() - t1))

            ret = self._procedure_output_list_type()
            ret.output_list = []
            return ret

    def Close(self):
        with self.parent._output_lock:
            self._closed = True
            self.parent._output_evt.notify_all()

    def Abort(self):
        with self.parent._output_lock:
            self._closed = True
            self.parent._output_evt.notify_all()
        




class PyriSandboxStoppedError(BaseException):
    pass

class ExecuteProcedureGenerator:

    def __init__(self, parent, procedure_name, byte_code, builtins, sandbox_globals,loc, params, print_collector, node, device_manager, status_type, run_number):
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
        self._run_number = run_number

    @property
    def procedure_name(self):
        return self._procedure_name

    @property
    def run_number(self):
        return self._run_number

    def Next(self):
        try:
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
                        self._loc[self._procedure_name]()
                    else:
                        self._loc[self._procedure_name](*self._params)

                    res = PyriSandboxContext.proc_result

                    assert isinstance(res,str) or res is None, "Result of procedure must be string"

                    ret = self._status_type()
                    # TODO: use constants
                    ret.action_status = 3
                    ret.printed = self._print_collector.printed
                    ret.result_code = res or "SUCCESS"
                    self._parent._send_print(f"Procedure \"{self._procedure_name}\" complete", self._procedure_name, self._parent._output_codes["status"])

                    return ret
            except PyriSandboxStoppedError:
                raise RR.OperationAbortedException("Procedure has been stopped")
            finally:
                sys.settrace(old_trace)
                self._parent._execution_complete(self)
        except BaseException as exp:
            if not isinstance(exp,RR.StopIterationException):
                self._parent._send_print(f"Execute procedure \"{self._procedure_name}\" failed:\n\n{traceback.format_exc()}",
                    self._procedure_name, self._parent._output_codes["error"])
            raise

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


       

        