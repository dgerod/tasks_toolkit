import time
import threading
import rospy
from .task import Task


class RunnableStateLock:

    _IDLE = 1
    _STARTING = 2
    _RUNNING = 3
    _STOPPING = 4
    _STOPPED = 5

    def __init__(self):

        self._lock = threading.Lock()
        self._state = self._IDLE

    def request_start(self):

        with self._lock:
            if self._state == self._IDLE:
                self._state = self._STARTING
                return True
            else:
                return False

    def request_stop(self):

        with self._lock:
            if self._state == self._RUNNING:
                self._state = self._STOPPING
                return True
            else:
                return False

    def notify_running(self):

        with self._lock:
            if self._state == self._STARTING:
                self._state = self._RUNNING
                return True
            else:
                return False

    def notify_stopped(self):

        with self._lock:
            if self._state == self._STOPPING:
                self._state = self._STOPPED
                return True
            else:
                return False

    def is_idle(self):

        with self._lock:
            state = self._state
        return state == self._IDLE

    def is_starting(self):

        with self._lock:
            state = self._state
        return state == self._STARTING

    def is_running(self):

        with self._lock:
            state = self._state
        return state == self._RUNNING

    def is_stopping(self):

        with self._lock:
            state = self._state
        return state == self._STOPPING

    def is_stopped(self):

        with self._lock:
            state = self._state
        return state == self._STOPPED


class Runnable(threading.Thread):

    _DEFAULT_REFRESH_TIME_SECONDS = 0.1

    def __init__(self, task:Task, refresh_time_in_seconds: float = _DEFAULT_REFRESH_TIME_SECONDS):

        super(Runnable, self).__init__()
        self._start_event = threading.Event()
        self._state = RunnableStateLock()
        self._task = task
        self._refresh_time = refresh_time_in_seconds

    def __del__(self):
        self._stop_and_wait()

    def start(self):
        self._start_and_wait()

    def stop(self):
        self._stop_and_wait()

    def run(self):

        rospy.logdebug("Runnable::run() - stat")

        if self._task.initialize():
            self._state.notify_running()
        else:
            return False

        rospy.logdebug("Runnable::run() - initialized")
        self._start_event.set()

        while self._state.is_running():
            rospy.logdebug("Runnable::run() - step")
            self._task.step()
            time.sleep(self._refresh_time)

        rospy.logdebug("Runnable::run() - finalizing")
        self._task.finalize()
        self._state.notify_stopped()

        rospy.logdebug("Runnable::run() - end")
        return True

    def _start_and_wait(self):
        if not self._state.request_start():
            return False
        else:
            threading.Thread.start(self)
            self._start_event.wait()
            return True

    def _stop_and_wait(self):
        rospy.logdebug("Runnable::_stop_and_wait()")
        if self._state.request_stop():
            rospy.logdebug("Runnable:_stop_and_wait() - joining")
            self.join()
            return True
        else:
            return False
