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

from blend import Paths


class TestPaths(unittest.TestCase):

    def test_paths_has_a_search_paths_property(self):
        env = Paths()
        self.assertNotEqual(None, env.search_paths)

    def test_default_path_property_value_is_an_array_containing_cwd(self):
        env = Paths()
        self.assertEqual([os.getcwd()], env.search_paths)

    def test_paths_can_be_created_with_search_paths(self):
        env = Paths('/tmp/test', '/tmp/lib')
        self.assertEqual(['/tmp/test', '/tmp/lib', os.getcwd()], env.search_paths)

    def test_cwd_can_be_omitted_from_paths(self):
        env = Paths('/tmp/test', '/tmp/lib', include_cwd=False)
        self.assertEqual(['/tmp/test', '/tmp/lib'], env.search_paths)

    def test_creating_with_none_results_in_cwd_as_the_only_path(self):
        env = Paths(None)
        self.assertEqual([os.getcwd()], env.search_paths)
