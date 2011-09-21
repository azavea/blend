import os

class Resource:
    """
    Representation of a file on disk
    """
    def __init__(self, pathToFile):
        """
        Arguments:
        pathToFile -- The path at which the physical file is/will be located.
        """
        if not pathToFile:
            raise Exception('Resource must be created with a pathToFile')
        if not isinstance(pathToFile, str):
            raise Exception('The pathToFile argument must be set to a string')

        self._pathToFile = pathToFile
        self._extension, self._filetype = Resource._parseExtensionAndFileType(pathToFile)
        self._baseName = Resource._parseBaseName(pathToFile)

    @staticmethod
    def _parseExtensionAndFileType(pathToFile):
        """
        Extract a lower case extension from the specified file name and return it
        along with a filetype string
        Arguments:
        pathToFile -- The full path to a file that may or may not exist.
        """
        basename, ext = os.path.splitext(pathToFile)
        ext = ext.lower()[1:]

        if ext == 'js' or ext == 'javascript':
            filetype = 'javascript'
        else:
            filetype = 'unknown'

        return (ext, filetype)

    @staticmethod
    def _parseBaseName(pathToFile):
        """
        Extract a lower case name from the specified pathToFile by removing the
        extension, '-min', and and version number if they are present.
        Arguments:
        pathToFile -- The full path to a file that may or may not exist.
        """
        directory, file = os.path.split(pathToFile)
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
    def pathToFile(self):
        """
        The path at which the physical file is/will be located.
        """
        return self._pathToFile

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