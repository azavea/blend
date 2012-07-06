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
import subprocess

from Minifier import Minifier
from helpers import first_file_name_in_path_matching_regex


class YUICompressorMinifier(Minifier):

    def __init__(self, lib_path=None):
        self._yuic_proc_args = None
        self._module_path = os.path.dirname(os.path.realpath(__file__))
        self._lib_path = lib_path or os.path.join(self._module_path, 'lib')
        self._yuic_jar_regex = re.compile(r'^yuicompressor.*\.jar$')
        self._yuic_jar_file_path = first_file_name_in_path_matching_regex(self._lib_path, self._yuic_jar_regex)

    def minify(self, resource):
        minification = Minifier.minify(self, resource)
        if self._yuic_jar_file_path is None:
            minification.mark_as_bad()
            minification.add_error('A YUI Compressor .jar file could not be found in %s.' % self._lib_path)
            return minification

        if resource.minified:
            minification.set_content(resource.content)
            minification.mark_as_good()
            minification.add_message('The resource %s is already minified.' % resource.path_to_file)
        else:
            yuic_proc_args = ["java", "-jar", self._yuic_jar_file_path, resource.path_to_file]
            yuic_proc = subprocess.Popen(yuic_proc_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            yuic_output = yuic_proc.communicate()

            if yuic_proc.returncode == 0:
                minification.set_content(yuic_output[0])
                minification.mark_as_good()
            else:
                minification.mark_as_bad()
                minification.add_error("The YUI Compressor had non-zero exit code: " + str(yuic_proc.returncode) +
                    "\n    " + str(yuic_proc_args) +
                    "\n    " + yuic_output[1])

        return minification
