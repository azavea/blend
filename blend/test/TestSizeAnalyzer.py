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
from blend import SizeAnalyzer, Analysis

class TestSizeAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = SizeAnalyzer()

    def tearDown(self):
        pass

    def test_analyze_method_produces_an_analysis_instance(self):
        analysis = self.analyzer.analyze('some text')
        self.assertIsNotNone(analysis)

    def test_analysis_is_always_good(self):
        analysis = self.analyzer.analyze('some text')
        self.assertTrue(analysis.good)

    def test_analysis_has_no_warnings_no_errors_and_one_message(self):
        analysis = self.analyzer.analyze('some text')
        self.assertIsNone(analysis.warnings)
        self.assertIsNone(analysis.errors)
        self.assertIsNotNone(analysis.messages)
        self.assertEqual(1, len(analysis.messages))

    def test_analysis_message_contatins_content_size_and_line_count(self):
        analysis = self.analyzer.analyze('some\ttext\non two lines')
        self.assertEqual('%d characters in %d lines' % (21, 2), analysis.messages[0])

    def test_analysis_converted_to_string_is_the_single_message(self):
        analysis = self.analyzer.analyze('some\ttext\non two lines')
        self.assertEqual(analysis.messages[0], str(analysis))
