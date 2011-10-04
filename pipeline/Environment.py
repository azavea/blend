import os

class Environment:

    def __init__(self):
        self._paths = [os.getcwd()]

    @property
    def paths(self):
        """
        The string name of the required resource
        """
        return self._paths