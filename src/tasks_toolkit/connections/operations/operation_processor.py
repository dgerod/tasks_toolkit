from .operation_connector import OperationConnectorLock
from .operation import Operation
from .operation_caller import OperationCaller


class OperationsExecutor(object):

    _OPERATION_CALLER_INDEX = 0

    def __init__(self):
        self._operations = dict()

    def register(self, name: str, operation: Operation):

        connector = OperationConnectorLock(operation)
        caller = OperationCaller(connector)
        self._operations[name] = (caller, connector)

    def execute(self):

        for key in self._operations.keys():
            connector = self._operations[key][1]
            success, operation, inputs = connector.notify_started()
            if success:
                status, outputs = operation.request(inputs)
                connector.notify_completed(status, outputs)

    def find_operation(self, name):

        if name in self._operations.keys():
            return self._operations[name][self._OPERATION_CALLER_INDEX]
        else:
            return None
