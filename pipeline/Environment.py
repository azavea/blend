import os

class Environment:

    def __init__(self, *args, **kwargs):
        self._paths = []
        for arg in args:
            self._paths.append(arg)
        if 'include_cwd' not in kwargs or ('include_cwd' in kwargs and kwargs['include_cwd']):
            self._paths.append(os.getcwd())
            
    @property
    def paths(self):
        """
        The string name of the required resource
        """
        return self._paths