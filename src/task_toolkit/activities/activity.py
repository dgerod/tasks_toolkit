from .runnable import Runnable
from .task import Task


class Activity:

    def __init__(self, task: Task):
        self._runnable = Runnable(task)

    def start(self):
        self._runnable.start()

    def stop(self):
        self._runnable.stop()


class ActivityFactory:

    class ActivityType:
        NORMAL = 1

    def make_activity(self, type_: ActivityType, task: Task):

        if type_ == self.ActivityType.NORMAL:
            return Activity(task)
        else:
            raise NotImplementedError("Selected activity type does not exist yet")
