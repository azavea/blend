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
import os
import shutil
import tempfile
from helpers import create_file_with_content
from blend import SizeAnalyzer, Resource


class TestSizeAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = SizeAnalyzer()
        self.test_env_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.test_env_dir, 'test_file.txt')
        create_file_with_content(self.test_file_path, 'some\ttext\non two lines')
        self.resource = Resource(self.test_file_path)

    def tearDown(self):
        shutil.rmtree(self.test_env_dir)

    def test_analyze_method_produces_an_analysis_instance(self):
        analysis = self.analyzer.analyze(self.resource)
        self.assertIsNotNone(analysis)

    def test_analysis_is_always_good(self):
        analysis = self.analyzer.analyze(self.resource)
        self.assertTrue(analysis.good)

    def test_analysis_has_no_warnings_no_errors_and_one_message(self):
        analysis = self.analyzer.analyze(self.resource)
        self.assertIsNone(analysis.warnings)
        self.assertIsNone(analysis.errors)
        self.assertIsNotNone(analysis.messages)
        self.assertEqual(1, len(analysis.messages))

    def test_analysis_message_contatins_char_count_line_count_and_file_size(self):
        analysis = self.analyzer.analyze(self.resource)
        self.assertEqual('%s: %d characters in %d lines for %d bytes' % (self.resource.path_to_file, 21, 2, 22), analysis.messages[0])

    def test_analysis_converted_to_string_is_the_single_message(self):
        analysis = self.analyzer.analyze(self.resource)
        self.assertEqual(analysis.messages[0], str(analysis))
