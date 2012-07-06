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
import inspect

from blend import *


class TestBlend(unittest.TestCase):
    """Assert that the blend module contains a set of expected classes and methods."""
    def test_blend_has_a_resource_class(self):
        inspect.isclass(Resource)

    def test_blend_has_a_requirement_class(self):
        inspect.isclass(Requirement)

    def test_blend_has_a_paths_class(self):
        inspect.isclass(Paths)

    def test_blend_has_an_application_class(self):
        inspect.isclass(Application)

    def test_blend_has_an_analyzer_class(self):
        inspect.isclass(Analyzer)

    def test_blend_has_an_analysis_class(self):
        inspect.isclass(Analysis)

    def test_blend_has_a_size_analyzer_class(self):
        inspect.isclass(SizeAnalyzer)

    def test_blend_has_a_configuration_class(self):
        inspect.isclass(Configuration)

    def test_blend_has_a_JSLintAnalyzerClass(self):
        inspect.isclass(JSLintAnalyzer)

    def test_blend_has_a_minifier_class(self):
        inspect.isclass(Minifier)

    def test_blend_has_a_Result_class(self):
        inspect.isclass(Result)

    def test_blend_has_a_minification_class(self):
        inspect.isclass(Minification)

    def test_blend_has_a_YUICompressorMinifier_class(self):
        inspect.isclass(YUICompressorMinifier)
