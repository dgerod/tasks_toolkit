
class Operation:

    def __init__(self, function):
        self._function = function

    def request(self, inputs):
        return self._function(inputs)
