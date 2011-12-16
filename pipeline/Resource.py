import os
import re
import shutil

from Requirement import Requirement
from Environment import Environment

class Resource:
    """
    Representation of a file on disk
    """
    def __init__(self, path_to_file):
        """
        Arguments:
        path_to_file -- The path at which the physical file is/will be located.
        """
        if not path_to_file:
            raise Exception('Resource must be created with a path_to_file')
        if not isinstance(path_to_file, str):
            raise Exception('The path_to_file argument must be set to a string')

        self._path_to_file = path_to_file
        self._extension, self._file_type = Resource._parse_extension_and_file_type(path_to_file)
        self._base_name = Resource._parse_base_name(path_to_file)
        self._set_content(path_to_file)
        self._set_requirements()

    def _set_content(self, path_to_file):
        """
        Reads the content of the file specified by path_to_file into the _content
        member variable.
        Arguments:
        path_to_file -- The path at which the physical file is be located.
        Remarks:
        If path_to_file specifies a non-existent file the _content member variable is
        set to None
        """
        if os.path.exists(path_to_file):
            f = open(path_to_file, 'r')
            try:
                self._content = f.read()
            finally:
                f.close()
        else:
            self._content = None

    def _set_requirements(self):
        """
        Parse the content of the file and set the _requirements member variable to a
        list Requirement objects.
        Remarks:
        Must be called AFTER _set_content() is called and after self._file_type is set.
        """
        self._requirements = None

        if self._file_type == 'unknown' or self._content is None:
            return

        if self._file_type == 'javascript':
            require_re = re.compile(r'[ \t]*//=[ \t]+require[ \t]+([<"])(\S+)[>"][ \t]*\n{0,1}')
        else: # 'css'
            require_re = re.compile(r'\@import url\((")(\S+)"\)')

        # This loop expects each match to have 2 groups. The first group captures the
        # punctuation mark around the file name and the second captures the name itself
        for result in require_re.finditer(self._content):
            if result.groups()[0] == '<':
                type = 'global'
            else:
                type = 'local'
            name = str(result.groups()[1])
            insert_position = (result.start(), result.end())
            if self._requirements is None:
                self._requirements = []
            self._requirements.append(Requirement(name, type, insert_position))

    @staticmethod
    def _parse_extension_and_file_type(path_to_file):
        """
        Extract a lower case extension from the specified file name and return it
        along with a file type string
        Arguments:
        path_to_file -- The full path to a file that may or may not exist.
        """
        base_name, ext = os.path.splitext(path_to_file)
        ext = ext.lower()[1:]

        if ext == 'js' or ext == 'javascript':
            file_type = 'javascript'
        elif ext == 'css':
            file_type = 'css'
        else:
            file_type = 'unknown'

        return ext, file_type

    @staticmethod
    def _parse_base_name(path_to_file):
        """
        Extract a lower case name from the specified path_to_file by removing the
        extension, '-min', and and version number if they are present.
        Arguments:
        path_to_file -- The full path to a file that may or may not exist.
        """
        directory, file = os.path.split(path_to_file)
        name, dot, extension =  file.rpartition('.')
        lower_name = name.lower()
        if lower_name[-4:] == '-min':
            lower_name = lower_name[:-4]
        lower_name_without_version, dash, version = lower_name.rpartition('-')
        if dash == '':
            return lower_name
        else:
            return lower_name_without_version

    @property
    def path_to_file(self):
        """
        The path at which the physical file is/will be located.
        """
        return self._path_to_file

    @property
    def exists(self):
        """
        Whether or not the file represented by the Resource exists on disk.
        """
        return os.path.exists(self.path_to_file)

    @property
    def content(self):
        """
        The contents of the file.
        """
        return self._content

    @property
    def extension(self):
        """
        The file name extension of the physical file in lower case without the '.' character.
        """
        return self._extension

    @property
    def file_type(self):
        """
        A lower case string describing the content of this file.
        Possible values: unknown, javascript, css.
        """
        return self._file_type

    @property
    def base_name(self):
        """
        The name of the resource with version numbers and minification designations removed.
        Example: OpenLayers.js -> openlayers
        Example: jQuery-1.5.4-min.js -> jquery
        """
        return self._base_name

    @property
    def requirements(self):
        """
        The descriptions of the the other resources on which this resource depends.
        """
        return self._requirements

    def merge_requirements_from_environemnt(self, environment):
        if self.requirements:
            merged_content = ''.join(self.content) # Get a copy of the content string
            # The requirements are parsed out of the file in order from top to bottom. If
            # you also merge the requirements in that order, the insert position of the second
            # requirement will be throw off by the merging of the first. Iterating over the list
            # in reverse order ensures merging multiple files into the same target will work correctly.
            for requirement in reversed(self.requirements):
                for resource in Resource.find_all_of_type_in_environment(self.file_type, environment):
                    if resource.base_name == requirement.name.lower():
                        merged_content = merged_content[:requirement.insert_location[0]] + \
                                         resource.merge_requirements_from_environemnt(environment) + \
                                         merged_content[requirement.insert_location[1]:]
                        break
            return merged_content
        else:
            return self.content

    @staticmethod
    def find_all_of_type_in_environment(file_type, environment):
        """
        Get a list of Resource instances representing all the files in the current working
        directory that have the specified file_type
        Arguments:
        file_type -- The string name of the type of file to be found. Can be unknown, javascript, or css
        environment -- An Environment instance defining where to search for files.
        Remarks:
        Calls find_all_of_type_in_path for each path in the environment.
        """
        resources = []
        for path in environment.paths:
            resources.extend(Resource._find_all_of_type_in_path(file_type, path))
        return resources if len(resources) > 0 else None

    @staticmethod
    def _find_all_of_type_in_path(file_type, path):
        """
        Get a list of Resource instances representing all the files in the specified
        directory (and sub-directories) that have the specified file_type
        Arguments:
        file_type -- The string name of the type of file to be found. Can be unknown, javascript, or css.
        path -- The base directory to be recursively searched for files.
        """
        resources = []
        for dir_path, dir_names, file_names in os.walk(path):
            for file_name in file_names:
                resource = Resource(os.path.join(dir_path, file_name))
                if resource.file_type == file_type:
                    resources.append(resource)
        return resources

    @staticmethod
    def find_all_in_environment(environment):
        """
        Get a list of Resource instances representing all the files in the specified
        environment that have a processable file type.
        Arguments:
        environment -- An Environment instance defining where to search for files.
        """
        resources = []
        for path in environment.paths:
            resources_in_path = []
            for dir_path, dir_names, file_names in os.walk(path):
                for file_name in file_names:
                    absolute_file_path = os.path.join(dir_path, file_name)
                    ext, file_type = Resource._parse_extension_and_file_type(absolute_file_path)
                    if file_type != 'unknown':
                        resources_in_path.append(Resource(absolute_file_path))
            resources.extend(resources_in_path)
        return resources if len(resources) > 0 else None