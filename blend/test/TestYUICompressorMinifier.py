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
from blend import YUICompressorMinifier, Resource


class TestYUICompressorMinifier(unittest.TestCase):

    def setUp(self):
        self.test_env_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_env_dir)

    def make_an_empty_js_file(self):
        test_file_path = os.path.join(self.test_env_dir, 'test.js')
        create_file_with_content(test_file_path, '')
        return test_file_path

    def make_a_js_file(self, content='var answer = 42;'):
        test_file_path = os.path.join(self.test_env_dir, 'test.js')
        create_file_with_content(test_file_path, content)
        return test_file_path

    def make_a_minified_js_file(self, separator='.'):
        test_file_path = os.path.join(self.test_env_dir, 'test%smin.js' % separator)
        create_file_with_content(test_file_path, 'var a=42;')
        return test_file_path

    def test_analysis_fails_when_lib_dir_is_not_found(self):
        invalid_lib_path = '/some/invalid/path'
        yuic = YUICompressorMinifier(lib_path=invalid_lib_path)
        test_resource = Resource(self.make_a_js_file())
        minification = yuic.minify(test_resource)
        self.assertFalse(minification.good, 'Expected the minification to be bad since the tools could not be found')
        self.assertEquals(1, len(minification.errors))
        self.assertEquals('A YUI Compressor .jar file could not be found in %s.' % invalid_lib_path, minification.errors[0])

    def test_minifying_an_empty_resource_returns_empty_minification_content(self):
        test_resource = Resource(self.make_an_empty_js_file())
        yuic = YUICompressorMinifier()
        minification = yuic.minify(test_resource)
        self.assertTrue(minification.good)
        self.assertEqual('', minification.content)

    def test_minifying_an_already_minified_resource_returns_a_message_and_unmodified_content(self):
        test_resource = Resource(self.make_a_minified_js_file())
        self.assertTrue(test_resource.minified)
        yuic = YUICompressorMinifier()
        minification = yuic.minify(test_resource)
        self.assertTrue(minification.good)
        self.assertEqual(test_resource.content, minification.content)
        self.assertEqual('The resource %s is already minified.' % test_resource.path_to_file,
            minification.errors_warnings_and_messages_as_string)

    def test_compressor(self):
        test_resource = Resource(self.make_a_js_file(
            content='var answer = 42;\nvar question = "what is " +\n "6 times 7";'))
        yuic = YUICompressorMinifier()
        minification = yuic.minify(test_resource)
        self.assertTrue(minification.good)
        self.assertEqual('var answer=42;var question="what is 6 times 7";', minification.content)

    def test_compressor_failure(self):
        test_resource = Resource(self.make_a_js_file(
            content='var obj = { function: "failure" }'))  # 'function' is not a legal property name
        yuic = YUICompressorMinifier()
        minification = yuic.minify(test_resource)
        self.assertFalse(minification.good)
