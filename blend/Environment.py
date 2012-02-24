import os

class Environment:
    """
    A container for all the paths that should be searched when attempting to locate
    required resources.
    """

    def __init__(self, *args, **kwargs):
        """
        Arguments:
        *args -- Directory paths which will be recursively searched for resources. Order
        is important because the first matching resource will be returned from a search.
        Paths will be searched in order from left to right.
        **kwargs -- Configuration options:
            include_cwd -- Boolean (default value is True) defining whether the current
            working directory will be searched after any other specified directories.
        """
        self._paths = []
        for arg in args:
            if arg is not None:
                self._paths.append(arg)
        if 'include_cwd' not in kwargs or ('include_cwd' in kwargs and kwargs['include_cwd']):
            self._paths.append(os.getcwd())

    @property
    def paths(self):
        """
        An ordered list of paths in which resources will be located.
        """
        return self._paths