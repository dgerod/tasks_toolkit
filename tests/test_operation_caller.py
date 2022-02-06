#!/usr/bin/env python

import unittest
from tasks_toolkit.connections.operations import OperationsExecutor
from tasks_toolkit.connections.operations \
    import Operation, OperationCaller, OperationHandler, OperationConnectorLock


class TestOperationCaller(unittest.TestCase):

    def _on_dummy_success(self, inputs):
        return True, None

    def _on_dummy_fails(self, inputs):
        return False, None

    def _on_dummy_with_inputs(self, inputs):
        return True, [inputs[1] + 1.0, inputs[0]]

    def test_operation_without_inputs_and_success(self):

        operations = OperationsExecutor()
        operations.register('dummy_success', Operation(self._on_dummy_success))

        operation = operations.find_operation('dummy_success')
        self.assertIsInstance(operation, OperationCaller)
        operation_handle = operation.request()
        self.assertIsInstance(operation_handle, OperationHandler)

        is_completed, results = operation_handle.collect_if_done()
        self.assertEqual(is_completed, False)

        operations.execute()
        is_completed, results = operation_handle.collect_if_done()
        self.assertEqual(is_completed, True)
        self.assertEqual(results[0], True)
        self.assertEqual(results[1], None)

    def test_operation_without_inputs_and_fails(self):

        operations = OperationsExecutor()
        operations.register('dummy_fails', Operation(self._on_dummy_fails))

        operation = operations.find_operation('dummy_fails')
        self.assertIsInstance(operation, OperationCaller)
        operation_handle = operation.request()
        self.assertIsInstance(operation_handle, OperationHandler)

        is_completed, results = operation_handle.collect_if_done()
        self.assertEqual(is_completed, False)

        operations.execute()
        is_completed, results = operation_handle.collect_if_done()
        self.assertEqual(is_completed, True)
        self.assertEqual(results[0], False)
        self.assertEqual(results[1], None)

    def test_operation_with_inputs(self):

        operations = OperationsExecutor()
        operations.register('dummy_with_inputs', Operation(self._on_dummy_with_inputs))

        operation = operations.find_operation('dummy_with_inputs')
        self.assertIsInstance(operation, OperationCaller)

        inputs = ('hello', 2)
        operation_handle = operation.request(inputs)
        self.assertIsInstance(operation_handle, OperationHandler)
        
        is_completed, results = operation_handle.collect_if_done()
        self.assertEqual(is_completed, False)

        operations.execute()
        success, outputs = operation_handle.collect()
        self.assertEqual(success, True)
        self.assertEqual(outputs, [3, 'hello'])

    def test_multiple(self):

        operations = OperationsExecutor()
        operations.register('dummy_success', Operation(self._on_dummy_success))
        operations.register('dummy_fails', Operation(self._on_dummy_fails))

        operation = operations.find_operation('dummy_success')
        self.assertIsInstance(operation, OperationCaller)
        operation_handle_1 = operation.request()
        self.assertIsInstance(operation_handle_1, OperationHandler)
        operation = operations.find_operation('dummy_fails')
        self.assertIsInstance(operation, OperationCaller)
        operation_handle_2 = operation.request()
        self.assertIsInstance(operation_handle_2, OperationHandler)

        is_completed, results = operation_handle_2.collect_if_done()
        self.assertEqual(is_completed, False)
        is_completed, results = operation_handle_1.collect_if_done()
        self.assertEqual(is_completed, False)

        operations.execute()

        success, outputs = operation_handle_2.collect()
        self.assertEqual(success, False)
        self.assertEqual(outputs, None)
        success, outputs = operation_handle_1.collect()
        self.assertEqual(success, True)
        self.assertEqual(outputs, None)


if __name__ == '__main__':
    unittest.main()
