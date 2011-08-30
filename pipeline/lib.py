class Resource:
    """
    Representation of a file on disk
    """
    def __init__(self, filename):
        """
        Arguments:
        filename -- The path at which the physical file is/will be located.
        """
        if not filename:
            raise Exception('Resource must be created with a filename')
        if not isinstance(filename, str):
            raise Exception('The filename argument must be set to a string')

        self._filename = filename

    @property
    def filename(self):
        """
        The path at which the physical file is/will be located.
        """
        return self._filename
