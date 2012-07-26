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
from blend import JSLintAnalyzer, Resource


class TestJSLintAnalyzer(unittest.TestCase):

    def setUp(self):
        self.test_env_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_env_dir)

    def make_a_js_file_with_no_lint(self):
        test_file_path = os.path.join(self.test_env_dir, 'test.js')
        create_file_with_content(test_file_path, 'var answer = 42;')
        return test_file_path

    def make_a_js_file_with_lint(self):
        test_file_path = os.path.join(self.test_env_dir, 'test.js')
        create_file_with_content(test_file_path, 'answer = 42;')  # missing 'var'
        return test_file_path

    def test_analysis_fails_when_lib_dir_is_not_found(self):
        jsl = JSLintAnalyzer(lib_path='/some/invalid/path', use_nodejs_if_available=False)
        test_resource = Resource(self.make_a_js_file_with_no_lint())
        analysis = jsl.analyze(test_resource)
        self.assertFalse(analysis.good, 'Expected the analysis to be bad since the tools could not be found')
        self.assertEquals(1, len(analysis.errors))
        self.assertEquals('No suitable JSLint runner (cscript.exe, node.js or rhino) could be found.', analysis.errors[0])

    def test_analysis_succeeds_for_resource_with_no_lint(self):
        jsl = JSLintAnalyzer()
        test_resource = Resource(self.make_a_js_file_with_no_lint())
        analysis = jsl.analyze(test_resource)
        self.assertTrue(analysis.good)

    def test_analysis_fails_for_resource_with_lint(self):
        jsl = JSLintAnalyzer()
        test_resource = Resource(self.make_a_js_file_with_lint())
        analysis = jsl.analyze(test_resource)
        self.assertFalse(analysis.good)
        self.assertEquals(1, len(analysis.errors))
