# By Justin Walgran
# Copyright (c) 2012 Azavea, Inc.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import os
import re
from copy import deepcopy

from Requirement import Requirement, RequirementNotSatisfiedException

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
        self._base_name, self._minified = Resource._parse_base_name_and_minification_status(path_to_file)
        self._set_content_and_size(path_to_file)
        self._set_requirements()

    def _set_content_and_size(self, path_to_file):
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
            self._size = os.path.getsize(path_to_file)
            f = open(path_to_file, 'r')
            try:
                self._content = f.read()
            finally:
                f.close()
        else:
            self._content = None
            self._size = 0

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
            require_re = re.compile(r'[ \t]*//=[ \t]+require[ \t]+([<"])(\S+)[>"][ \t]*\n?')
        else: # 'css'
            require_re = re.compile(r'@import url\((?P<import_punc>")(?P<import_match>\S+)\.\S+"\)|[ \t]*/\*=[ \t]+require[ \t]+(?P<require_punc>[<"])(?P<require_match>\S+)[>"][ \t]*\*/\n?')

        # This loop expects each match to have 2 groups. The first group captures the
        # punctuation mark around the file name and the second captures the name itself
        for result in require_re.finditer(self._content):
            if self._file_type == 'javascript':
                punc = result.groups()[0]
                name = str(result.groups()[1])
            else:
                punc = result.group('import_punc') or result.group('require_punc')
                if result.group('import_match') is not None:
                    name = str(result.group('import_match'))
                else:
                    name = str(result.group('require_match'))

            if punc == '<':
                type = 'global'
            else:
                type = 'local'

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
    def _parse_base_name_and_minification_status(path_to_file):
        """
        Extract a lower case name from the specified path_to_file by removing the
        extension, '-min', and and version number if they are present.
        Arguments:
        path_to_file -- The full path to a file that may or may not exist.
        """
        directory, file = os.path.split(path_to_file)
        name, dot, extension =  file.rpartition('.')
        lower_name = name.lower()
        minified = False
        if lower_name[-4:] == '-min' or lower_name[-4:] == '.min':
            lower_name = lower_name[:-4]
            minified = True
        lower_name_without_version, dash, version = lower_name.rpartition('-')
        if dash == '':
            return lower_name, minified
        else:
            return lower_name_without_version, minified

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
    def size(self):
        """
        The path at which the physical file is/will be located.
        """
        return self._size

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
    def minified(self):
        return self._minified

    @property
    def requirements(self):
        """
        The descriptions of the the other resources on which this resource depends.
        """
        return self._requirements

    def get_chunks_by_merging_requirements_from_environment(self, environment, previously_merged):
        if self.requirements:
            map = self.map_requirements(environment, map={}, previously_required=[])

            chunks_and_requirements = []
            position = 0

            for requirement in self.requirements:
                if (position == 0 and requirement.insert_location[0] > 0) or position != requirement.insert_location[0]:
                    chunks_and_requirements.append(Chunk(self, position, requirement.insert_location[0]))
                chunks_and_requirements.append(requirement)
                position = requirement.insert_location[1]
            if position < len(self.content):
                chunks_and_requirements.append(Chunk(self, position))

            chunks = []
            for chunk_or_requirement in chunks_and_requirements:
                if isinstance(chunk_or_requirement, Requirement):
                    resource = map[chunk_or_requirement.standard_name]['resource']
                    if resource.base_name not in previously_merged:
                        chunks = chunks + resource.get_chunks_by_merging_requirements_from_environment(environment, previously_merged)
                    previously_merged.append(resource.base_name)
                else:
                    chunks.append(chunk_or_requirement)

            return chunks
        else:
            return [Chunk(self)]

    def merge_requirements_from_environment(self, environment, previously_merged):
        chunks = self.get_chunks_by_merging_requirements_from_environment(environment, previously_merged)
        return ''.join([chunk.content for chunk in chunks])

    def map_requirements(self, environment, map, previously_required):
        if self.requirements:
            for requirement in self.requirements:
                map[requirement.standard_name] = None
                if requirement.type == 'global':
                    resources_of_the_same_type = Resource.find_all_of_type_in_environment(self.file_type, environment)
                else: # requirement.type == 'local'
                    resources_of_the_same_type = Resource.find_all_of_type_in_path(self.file_type, os.path.dirname(self.path_to_file))

                if resources_of_the_same_type is not None:
                    for resource in resources_of_the_same_type:
                        if resource.base_name == requirement.standard_name:
                            new_previously_required = deepcopy(previously_required)
                            new_previously_required.append(requirement.standard_name)
                            resource.map_requirements(environment, map, new_previously_required)

                            map[requirement.standard_name] = {
                                'resource': resource,
                                'previously_required': deepcopy(previously_required)
                            }

                if not map[requirement.standard_name]:
                    raise RequirementNotSatisfiedException(requirement, environment)

        return map



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
            resources.extend(Resource.find_all_of_type_in_path(file_type, path, skip_path=environment.output_path))
        return resources if len(resources) > 0 else None

    @staticmethod
    def find_all_of_type_in_path(file_type, path, skip_path=None):
        """
        Get a list of Resource instances representing all the files in the specified
        directory (and sub-directories) that have the specified file_type
        Arguments:
        file_type -- The string name of the type of file to be found. Can be unknown, javascript, or css.
        path -- The base directory to be recursively searched for files.
        """
        resources = []
        for dir_path, dir_names, file_names in os.walk(path):
            if os.path.abspath(dir_path) != os.path.abspath(skip_path):
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

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.base_name

class Chunk():
    def __init__(self, resource, start=None, end=None):
        self._resource = resource
        self._start = start
        self._end = end

    @property
    def resource(self):
        return self._resource

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        value = self.resource.base_name
        if self.start is not None:
            value = value + ':' + self.start
        if self.end is not None:
            value = value + ':' + self.end
        return value

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def content(self):
        return self._resource.content[self._start:self._end]