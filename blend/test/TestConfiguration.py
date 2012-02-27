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

import unittest

from blend import Configuration
from blend import Analyzer
from blend.SizeAnalyzer import SizeAnalyzer

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_can_add_analyzer_for_filetype(self):
        conf = Configuration()
        analyzer = Analyzer()
        conf.add_analyzer_for_file_type(analyzer, 'javascript')
        analyzers = conf.get_analyzers_for_file_type('javascript')
        self.assertListEqual([analyzer], analyzers)

    def test_add_analyzer_checks_classes(self):
        conf = Configuration()
        self.assertRaises(Exception, conf.add_analyzer_for_file_type, 'string instead of an analyzer', 'javascript')

        # should not throw
        conf.add_analyzer_for_file_type(Analyzer(), 'javascript')
        # should not throw
        conf.add_analyzer_for_file_type(SizeAnalyzer(), 'javascript')