import interface
from ..activities import Task


class ExecutionEngine(interface.implements(Task)):

    def __init__(self):
        pass

    def _step(self):
        self._execute_operations()
        self._read_input_ports()
        self._do_logic()
        self._write_output_ports()

    def _execute_operations(self):
        self._operations.process()

    def _read_input_ports(self):
        pass

    def _do_logics(self):
        pass

    def _write_output_ports(self):
        pass
