import unittest

from pipeline import Requirement

class TestRequirement(unittest.TestCase):

    def test_requirement_must_be_created_with_a_name_and_a_type(self):
        self.assertRaises(Exception, Requirement)
        self.assertRaises(Exception, Requirement, 'name but not type')
        self.assertRaises(Exception, Requirement, None, None)
        # This call to the constructor should not raise an exception
        Requirement('name', 'local')

    def test_requirement_name_must_be_a_string(self):
        self.assertRaises(Exception, Requirement, 1, 'local')

    def test_requirement_type_must_be_a_string(self):
        self.assertRaises(Exception, Requirement, 'name', 1)

    def test_requirement_type_must_be_local_or_global(self):
        # These two constructor calls should not throw an exception
        Requirement('name', 'local')
        Requirement('name', 'global')
        self.assertRaises(Exception, Requirement, 'name', 'foo')
