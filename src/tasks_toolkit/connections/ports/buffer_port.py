import threading


class BufferStorageLock:

    DEFAULT_MAX_SIZE = 1

    def __init__(self, max_size=DEFAULT_MAX_SIZE):

        self._lock = threading.Lock()
        self._max_size = max_size
        self._queue = []

    def push(self, element):

        with self._lock:
            if len(self._queue) < self._max_size:
                self._queue.append(element)

    def pop(self):

        element = None
        with self._lock:
            if self._queue:
                element = self._queue.pop()
        return element

    def pop_all(self):

        with self._lock:
            elements = tuple(self._queue)
            self._queue.clear()
        return elements


class InputBufferPort:

    def __init__(self, storage: BufferStorageLock):
        self._storage = storage

    def pop(self):
        return self._storage.pop()

    def pop_all(self):
        return self._storage.pop_all()


class OutputBufferPort:

    def __init__(self, storage: BufferStorageLock):
        self._storage = storage

    def push(self, data):
        return self._storage.push(data)
