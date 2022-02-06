import threading


class DataStorageLock:

    def __init__(self):

        self._lock = threading.Lock()
        self._data = None

    def write(self, data):

        with self._lock:
            self._data = data

    def read(self):

        with self._lock:
            data = self._data
        return data


class InputDataPort:

    def __init__(self, storage: DataStorageLock):
        self._storage = storage

    def read(self):
        return self._storage.read()


class OutputDataPort:

    def __init__(self, storage: DataStorageLock):
        self._storage = storage

    def write(self, data):
        return self._storage.write(data)
