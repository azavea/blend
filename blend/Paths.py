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


class Paths:
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
        self._search_paths = []
        for arg in args:
            if arg is not None:
                self._search_paths.append(arg)
        if 'include_cwd' not in kwargs or ('include_cwd' in kwargs and kwargs['include_cwd']):
            self._search_paths.append(os.getcwd())

        if 'output_path' in kwargs:
            self._output_path = kwargs['output_path']
        else:
            self._output_path = os.path.join(os.getcwd(), 'output')

    @property
    def search_paths(self):
        """
        An ordered list of paths in which resources will be located.
        """
        return self._search_paths

    @property
    def output_path(self):
        """
        An ordered list of paths in which resources will be located.
        """
        return self._output_path
