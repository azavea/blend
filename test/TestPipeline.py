import unittest
import inspect

from pipeline import *

class TestPipeline(unittest.TestCase):
    """Assert that the Pipeline module contains a set of expected classes and methods."""
    def testPipelineHasAResourceClass(self):
        inspect.isclass(Resource)