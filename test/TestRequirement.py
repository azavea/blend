import unittest

from pipeline import Requirement

class TestRequirement(unittest.TestCase):

    def test_requirement_must_be_created_with_a_name_and_a_type(self):
        self.assertRaises(Exception, Requirement)
        self.assertRaises(Exception, Requirement, 'name but not type')
        self.assertRaises(Exception, Requirement, None, None)
        requirement = Requirement('name', 'local')
        self.assertEqual('name', requirement.name)
        self.assertEqual('local', requirement.type)

    def test_requirement_name_must_be_a_string(self):
        self.assertRaises(Exception, Requirement, 1, 'local')

    def test_requirement_type_must_be_a_string(self):
        self.assertRaises(Exception, Requirement, 'name', 1)

    def test_requirement_type_must_be_local_or_global(self):
        # These two constructor calls should not throw an exception
        Requirement('name', 'local')
        Requirement('name', 'global')
        self.assertRaises(Exception, Requirement, 'name', 'foo')

    def test_requirement_has_a_default_insert_location(self):
        requirement = Requirement('name', 'local')
        self.assertEqual(0, requirement.insert_location)

    def test_requirement_takes_insert_location_as_an_optional_parameter(self):
        requirement = Requirement('name', 'local', 1)
        self.assertEqual(1, requirement.insert_location)
        requirement = Requirement('name', 'local', (10,22))
        self.assertEqual((10,22), requirement.insert_location)

    def test_insert_location_must_not_be_a_string(self):
        self.assertRaises(Exception, Requirement, 'name', 'local', 'some string')