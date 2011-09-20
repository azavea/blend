import os

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

    @property
    def extension(self):
        """
        The file name extension of the physical file in lower case without the '.' character
        """
        basename, ext = os.path.splitext(self.filename)
        return ext.lower()[1:]

    @property
    def filetype(self):
        """
        A lower case string describing the content of this file.
        Possible values: unknown, javascript
        """
        if self.extension == 'js' or self.extension == 'javascript':
            return 'javascript'
        else:
            return 'unknown'

    @property
    def baseName(self):
        """
        The name of the resource with version numbers and minification designations removed/
        """
        name, dot, extension =  self.filename.rpartition('.')
        lowerName = name.lower()
        if lowerName[-4:] == '-min':
            lowerName = lowerName[:-4]
        lowerNameWithoutVersion, dash, version = lowerName.rpartition('-')
        if dash == '':
            return lowerName
        else:
            return lowerNameWithoutVersion
