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
import tempfile

import helpers
import shutil
import os
import sys
from blend import Application

class TestApplication(unittest.TestCase):

    def setUp(self):
        self.test_env_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_env_dir)
        helpers.clean_output()

    def test_default_env_is_cwd(self):
        app = Application()
        self.assertEquals(app.paths.search_paths, [os.getcwd()])

    def test_default_include_cwd_is_true(self):
        app = Application()
        self.assertTrue(app.include_cwd)

    def test_default_file_list_is_empty(self):
        app = Application()
        self.assertEqual([], app.file_list)

    def test_default_output_dir_is_cwd_plus_output(self):
        app = Application()
        self.assertEqual(os.path.join(os.getcwd(), 'output'),  app.output_dir)

    def test_run_without_arguments_returns_zero(self):
        app = Application()
        self.assertEqual(0, app.run())

    def test_run_with_single_resource(self):
        paths_to_processable_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js')]
        helpers.create_test_files(paths_to_processable_test_files)
        app = Application(file_list=[paths_to_processable_test_files[0]])
        self.assertEqual(0, app.run())
        helpers.clean_up_test_files(paths_to_processable_test_files)

    def test_run_with_single_resource_with_requirement(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.js')]
        helpers.clean_up_test_files(paths_to_test_files)
        helpers.create_test_files(paths_to_test_files)
        helpers.create_test_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require file2')
        helpers.create_test_file_with_content(paths_to_test_files[1], '// This is file 2')
        app = Application(path_list=[self.test_env_dir], file_list=[paths_to_test_files[0]])
        self.assertEqual(0, app.run())
        helpers.clean_up_test_files(paths_to_test_files)

    @unittest.skipIf(len(sys.argv) > 1, "If arguments are passed to the unit test runner, this test fails")
    def test_main_exits_cleanly_when_no_args_are_passed(self):
        app = Application
        try:
            app.main()
        except SystemExit, system_exit_exception:
            self.assertEquals(0, system_exit_exception.code)