import unittest
import inspect

from blend import *

class TestBlend(unittest.TestCase):
    """Assert that the blend module contains a set of expected classes and methods."""
    def test_blend_has_a_resource_class(self):
        inspect.isclass(Resource)
        
    def test_blend_has_a_requirement_class(self):
        inspect.isclass(Requirement)

    def test_blend_has_an_environment_class(self):
        inspect.isclass(Environment)

    def test_blend_has_an_application_class(self):
        inspect.isclass(Application)