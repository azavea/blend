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
import json

from Analyzer import Analyzer
from Minifier import Minifier

class Configuration():

    def __init__(self, config_file_path=None):
        self.analyzers = None
        self.minifiers = None
        if config_file_path is not None:
            if not os.path.exists(config_file_path):
                raise Exception('Config file "%s" does not exist or is not accessible.' % config_file_path)
            f = open(config_file_path, 'r')
            try:
                configuration_dict = json.load(f)
            finally:
                f.close()
            if 'analyzers' in configuration_dict:
                analyzer_dict = configuration_dict['analyzers']
                for file_type in analyzer_dict.iterkeys():
                    analyzer_name_list = analyzer_dict[file_type]
                    for analyzer_name in analyzer_name_list:
                        analyzer_class = self._get_class(analyzer_name)
                        self.add_analyzer_for_file_type(analyzer_class(), file_type)

    def _get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    def add_analyzer_for_file_type(self, analyzer, file_type):
        if not isinstance(analyzer, Analyzer):
            raise Exception('You must pass and Analyzer instance')
        if self.analyzers is None:
            self.analyzers = {}
        if file_type not in self.analyzers:
            self.analyzers[file_type] = []
        if analyzer not in self.analyzers[file_type]:
            self.analyzers[file_type].append(analyzer)

    def get_analyzers_for_file_type(self, file_type):
        if self.analyzers is None: return None

        if file_type in self.analyzers:
            return self.analyzers[file_type]
        else:
            return None

    def set_minifier_for_file_type(self, minifier, file_type):
        if not isinstance(minifier, Minifier):
            raise Exception('You must pass a Minifier instance')
        if self.minifiers is None:
            self.minifiers = {}
        self.minifiers[file_type] = minifier

    def get_minifier_for_file_type(self, file_type):
        if self.minifiers is None:
            return None

        if file_type in self.minifiers:
            return self.minifiers[file_type]
        else:
            return None
