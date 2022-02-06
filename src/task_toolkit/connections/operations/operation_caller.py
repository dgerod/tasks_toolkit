from typing import Union
import time
from .operation_connector import OperationConnectorLock


class Operation:

    def __init__(self, function):
        self._function = function

    def request(self, inputs):
        return self._function(inputs)


class OperationHandler:

    def __init__(self, connector: OperationConnectorLock, refresh_time_in_seconds: float):

        self._connector = connector
        self._refresh_time = refresh_time_in_seconds

    def disconnect(self):
        pass

    def collect_if_done(self):
        return self._connector.is_completed(), self._connector.get_results()

    def collect(self, timeout_in_seconds=None):

        current_time = 0.0
        is_timeout_enabled = timeout_in_seconds is not None

        while (not self._connector.is_completed()
               and (True if not is_timeout_enabled else current_time < timeout_in_seconds)):
            time.sleep(self._refresh_time)
            current_time += self._refresh_time

        return self._connector.get_results()


class OperationCaller:

    _DEFAULT_REFRESH_TIME_SECONDS = 0.5

    def __init__(self, connector: OperationConnectorLock):
        self._connector = connector

    def execute(self, inputs):
        return NotImplementedError("Functionality not available yet")

    def request(self, inputs, refresh_time_in_second: float = _DEFAULT_REFRESH_TIME_SECONDS) \
            -> Union[OperationHandler, None]:

        if self._connector.add_request(inputs):
            return OperationHandler(self._connector, refresh_time_in_second)
        else:
            return None
