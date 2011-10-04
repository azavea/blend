import unittest
import inspect

from pipeline import *

class TestPipeline(unittest.TestCase):
    """Assert that the Pipeline module contains a set of expected classes and methods."""
    def test_pipeline_has_a_resource_class(self):
        inspect.isclass(Resource)
        
    def test_pipeline_has_a_requirement_class(self):
        inspect.isclass(Requirement)

    def test_pipeline_has_an_environment_class(self):
        inspect.isclass(Environment)