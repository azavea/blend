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
from blend import Analyzer, Analysis

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = Analyzer()

    def tearDown(self):
        pass

    def test_has_an_analyze_method(self):
        self.analyzer.analyze('some text')

    def test_analyze_method_produces_an_analysis_instance(self):
        analysis = self.analyzer.analyze('some text')
        self.assertIsNotNone(analysis)
        self.assertIsInstance(analysis, Analysis)

    def test_analysis_has_a_messages_property(self):
        analysis = self.analyzer.analyze(None)
        self.assertIsNone(analysis.messages)

    def test_analysis_has_a_warnings_property(self):
        analysis = self.analyzer.analyze(None)
        self.assertIsNone(analysis.warnings)

    def test_analysis_has_an_errors_property(self):
        analysis = self.analyzer.analyze(None)
        self.assertIsNone(analysis.errors)