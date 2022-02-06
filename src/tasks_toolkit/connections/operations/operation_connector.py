import threading


class OperationConnectorLock:

    _IDLE = 1
    _READY = 2
    _RUNNING = 3
    _COMPLETED = 4

    class Data:

        def __init__(self, operation):
            self.operation = operation
            self.inputs = None
            self.outputs = None
            self.status = None

        def set_inputs(self, inputs):
            self.inputs = inputs

        def set_results(self, status, outputs):
            self.status = status
            self.outputs = outputs

    def __init__(self, operation: Operation):

        self._lock = threading.Lock()
        self._data = self.Data(operation)
        self._state = self._IDLE

    def add_request(self, inputs):

        with self._lock:
            if (self._state == self._IDLE
                    or self._state == self._COMPLETED):
                self._state = self._READY
                self._data.set_inputs(inputs)
                return True
            return False

    def notify_started(self):

        with self._lock:
            if self._state == self._READY:
                self._state = self._RUNNING
                return True, self._data.operation, self._data.inputs
            else:
                return False, None, None

    def notify_completed(self, status, outputs):

        with self._lock:
            if self._state == self._RUNNING:
                self._state = self._COMPLETED
                self._data.set_results(status, outputs)
                return True
            else:
                return False

    def is_completed(self):
        with self._lock:
            state = self._state
        return state == self._COMPLETED

    def get_results(self):
        with self._lock:
            status = self._data.status
            outputs = self._data.outputs
        return status, outputs
