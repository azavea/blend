import os
import unittest
import tempfile
import shutil

from helpers import *
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