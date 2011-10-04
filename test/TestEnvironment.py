import unittest
import os

from pipeline import Environment

class TestEnvironment(unittest.TestCase):

    def test_environment_has_a_paths_property(self):
        env = Environment()
        self.assertNotEqual(None, env.paths)

    def test_default_path_property_value_is_an_array_containing_cwd(self):
        env = Environment()
        self.assertEqual([os.getcwd()], env.paths)

    def test_environment_can_be_created_with_paths(self):
        env = Environment('/tmp/test', '/tmp/lib')
        self.assertEqual(['/tmp/test', '/tmp/lib', os.getcwd()], env.paths)

    def test_cwd_can_be_omitted_from_paths(self):
        env = Environment('/tmp/test', '/tmp/lib', include_cwd = False)
        self.assertEqual(['/tmp/test', '/tmp/lib'], env.paths)