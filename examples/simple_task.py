#! /usr/bin/env python

import time
import interface
from tasks_toolkit.activities import Task, ActivityFactory


class CounterTask(interface.implements(Task)):

    def __init__(self):
        self._counter = 0

    def step(self):
        self._counter += 1
        print("counter: %d" % self._counter)


def main():

    activity = ActivityFactory().make_activity(ActivityFactory.ActivityType.NORMAL,
                                               CounterTask())
    activity.start()

    time.sleep(10)
    activity.stop()


if __name__ == "__main__":
    main()

