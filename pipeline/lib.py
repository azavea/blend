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
        self._extension, self._filetype = Resource._parseExtensionAndFileType(filename)
        self._baseName = Resource._parseBaseName(filename)

    @staticmethod
    def _parseExtensionAndFileType(filename):
        """
        Extract a lower case extension from the specified file name and return it
        along with a filetype string
        Arguments:
        filename -- The full path to a file that may or may not exist.
        """
        basename, ext = os.path.splitext(filename)
        ext = ext.lower()[1:]

        if ext == 'js' or ext == 'javascript':
            filetype = 'javascript'
        else:
            filetype = 'unknown'

        return (ext, filetype)

    @staticmethod
    def _parseBaseName(filename):
        """
        Extract a lower case name from the specified filename by removing the
        extension, '-min', and and version number if they are present.
        Arguments:
        filename -- The full path to a file that may or may not exist.
        """
        directory, file = os.path.split(filename)
        name, dot, extension =  file.rpartition('.')
        lowerName = name.lower()
        if lowerName[-4:] == '-min':
            lowerName = lowerName[:-4]
        lowerNameWithoutVersion, dash, version = lowerName.rpartition('-')
        if dash == '':
            return lowerName
        else:
            return lowerNameWithoutVersion

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
        return self._extension

    @property
    def filetype(self):
        """
        A lower case string describing the content of this file.
        Possible values: unknown, javascript
        """
        return self._filetype

    @property
    def baseName(self):
        """
        The name of the resource with version numbers and minification designations removed/
        """
        return self._baseName
