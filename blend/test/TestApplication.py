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

import shutil
import os
import sys
from blend import Application
from helpers import create_files, create_file_with_content, clean_up_files, clean_output


class TestApplication(unittest.TestCase):

    def setUp(self):
        self.test_env_dir = tempfile.mkdtemp()
        self.test_config_file_path = os.path.join(self.test_env_dir, 'config.json')
        self.default_config_file_path = os.path.join(os.getcwd(), '.blend', 'config.json')
        if os.path.exists(self.default_config_file_path):
            shutil.rmtree(os.path.dirname(self.default_config_file_path))

    def tearDown(self):
        shutil.rmtree(self.test_env_dir)
        if os.path.exists(self.default_config_file_path):
            shutil.rmtree(os.path.dirname(self.default_config_file_path))
        clean_output()

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
        create_files(paths_to_processable_test_files)
        app = Application(file_list=[paths_to_processable_test_files[0]])
        self.assertEqual(0, app.run())
        clean_up_files(paths_to_processable_test_files)

    def test_run_with_single_resource_with_requirement(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.js')]
        clean_up_files(paths_to_test_files)
        create_files(paths_to_test_files)
        create_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require file2')
        create_file_with_content(paths_to_test_files[1], '// This is file 2')
        app = Application(path_list=[self.test_env_dir], file_list=[paths_to_test_files[0]])
        self.assertEqual(0, app.run())
        clean_up_files(paths_to_test_files)

    @unittest.skipIf(len(sys.argv) > 1, "If arguments are passed to the unit test runner, this test fails")
    def test_main_exits_cleanly_when_no_args_are_passed(self):
        app = Application
        try:
            app.main()
        except SystemExit, system_exit_exception:
            self.assertEquals(0, system_exit_exception.code)

    def test_application_can_be_created_with_a_config_file_path(self):
        clean_up_files(self.test_config_file_path)
        create_file_with_content(self.test_config_file_path, '{}')
        Application(config_file_path=self.test_config_file_path)

    def test_loads_config_from_file(self):
        # To ensure that somthing is actually being tested, I first assert that the default configuration
        # is non-empty
        app = Application()
        self.assertTrue(app.config.analyzers, "expected the default analyzer list to be non-empty")
        self.assertTrue(app.config.minifiers, "expected the default minifier list to be non-empty")

        clean_up_files(self.test_config_file_path)
        create_file_with_content(self.test_config_file_path, '{}')
        app = Application(config_file_path=self.test_config_file_path)
        self.assertIsNotNone(app.config)
        self.assertFalse(app.config.analyzers, "expected the analyzer list to be empty")
        self.assertFalse(app.config.minifiers, "expected the minifier list to be empty")

    def test_loads_config_from_default_file_in_the_dot_blend_directory(self):
        # To ensure that somthing is actually being tested, I first assert that the default configuration
        # is non-empty
        app = Application()
        self.assertTrue(app.config.analyzers, "expected the default analyzer list to be non-empty")
        self.assertTrue(app.config.minifiers, "expected the default minifier list to be non-empty")

        clean_up_files(self.default_config_file_path)
        create_file_with_content(self.default_config_file_path, '{}')

        app = Application()
        self.assertIsNotNone(app.config)
        self.assertFalse(app.config.analyzers, "expected the analyzer list to be empty")
        self.assertFalse(app.config.minifiers, "expected the minifier list to be empty")

    def tests_config_file_passed_as_an_argument_overrides_the_file_in_dot_blend(self):
        # Step 1: Assert the default configuration with no config files
        app = Application()
        self.assertTrue(app.config.analyzers, "expected the default analyzer list to be non-empty")
        self.assertTrue(app.config.minifiers, "expected the default minifier list to be non-empty")

        # Step 2: Assert that config is loaded from .blend/config.json
        clean_up_files(self.default_config_file_path)
        create_file_with_content(self.default_config_file_path, '{}')

        app = Application()
        self.assertIsNotNone(app.config)
        self.assertFalse(app.config.analyzers, "expected the analyzer list to be empty")
        self.assertFalse(app.config.minifiers, "expected the minifier list to be empty")

        # Step 3: Assert that a custom config file overrides .blend/config.json
        clean_up_files(self.test_config_file_path)
        create_file_with_content(self.test_config_file_path, """{
    "analyzers": {
        "javascript": [
            {
                "name": "blend.SizeAnalyzer",
                "skip_list": [
                    "bin"
                ]
            }
        ]
    }
}""")
        app = Application(config_file_path=self.test_config_file_path)
        self.assertIsNotNone(app.config)
        self.assertEqual(1, len(app.config.analyzers), "expected one analyzer")
        self.assertFalse(app.config.minifiers, "expected the minifier list to be empty")
