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