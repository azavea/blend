import unittest
import tempfile

from pipeline.test.helpers import *
from pipeline import Application

class TestApplication(unittest.TestCase):

    def setUp(self):
        self.test_env_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_env_dir)
        clean_output()

    def test_default_env_is_cwd(self):
        app = Application()
        self.assertEquals(app.environment.paths, [os.getcwd()])

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
        create_test_files(paths_to_processable_test_files)
        app = Application(file_list=[paths_to_processable_test_files[0]])
        self.assertEqual(0, app.run())
        clean_up_test_files(paths_to_processable_test_files)

    def test_run_with_single_resource_with_requirement(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.js')]
        clean_up_test_files(paths_to_test_files)
        create_test_files(paths_to_test_files)
        create_test_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require <file2>')
        create_test_file_with_content(paths_to_test_files[1], '// This is file 2')
        app = Application(env_path_list=[self.test_env_dir], file_list=[paths_to_test_files[0]])
        self.assertEqual(0, app.run())
        clean_up_test_files(paths_to_test_files)

    def test_main_exits_cleanly_when_no_args_are_passed(self):
        app = Application
        try:
            app.main()
        except SystemExit, system_exit_exception:
            self.assertEquals(0, system_exit_exception.code)