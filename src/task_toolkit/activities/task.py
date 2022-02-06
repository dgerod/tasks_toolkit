import interface


class Task(interface.Interface):

    @interface.default
    def initialize(self):
        return True

    def step(self):
        pass

    @interface.default
    def finalize(self):
        return False
