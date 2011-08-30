import unittest

from pipeline import Resource

class TestResource(unittest.TestCase):
    """Asserts that the properties and methods of the Resource class behave correctly."""

    def testResourceMustBeCreatedWithAFileName(self):
        self.assertRaises(Exception, Resource)

    def testResourceMustBeCreatedWithAStringFilename(self):
        self.assertRaises(Exception, Resource, 1)

    def testResourceHasFilenamePropertySetOnInit(self):
        testFileName = 'some/file/name.txt'
        resource = Resource(testFileName)
        self.assertEqual(testFileName, resource.filename)