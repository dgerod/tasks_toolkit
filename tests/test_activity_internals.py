#!/usr/bin/env python

import unittest
from tasks_toolkit.activities.runnable import RunnableStateLock


class TestActivity(unittest.TestCase):

    def test_state_flow(self):

        activity_state = RunnableStateLock()
        self.assertEqual(activity_state.is_idle(), True)

        self.assertEqual(activity_state.request_start(), True)
        self.assertEqual(activity_state.is_starting(), True)

        self.assertEqual(activity_state.notify_running(), True)
        self.assertEqual(activity_state.is_running(), True)

        self.assertEqual(activity_state.request_stop(), True)
        self.assertEqual(activity_state.is_stopping(), True)

        self.assertEqual(activity_state.notify_stopped(), True)
        self.assertEqual(activity_state.is_stopped(), True)

    def test_activity_make(self):

        pass


if __name__ == '__main__':
    unittest.main()
