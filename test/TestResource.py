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

    def testResourceHasFileTypePropertyWithADefaultValueOfUnknown(self):
        testFileName = 'someFile'
        resource = Resource(testFileName)
        self.assertEqual('unknown', resource.filetype)

    def testResourceHasAnExtensionProperty(self):
        testFileNamesAndExpectedExtensions = [
            ('someFile.js',            'js'),
            ('someFile.JS',            'js'),
            ('noExtension',            ''),
            ('someFile.SomECraZytype', 'somecrazytype')]
        for testFileName, expectedExtension in testFileNamesAndExpectedExtensions:
            resource = Resource(testFileName)
            self.assertEqual(expectedExtension, resource.extension, 'Expected the extension of "' +
                testFileName + '" to be "' + expectedExtension + '"')

    def testResourceDetectsFileTypeByExtension(self):
        testFileNamesAndExpectedFileTypes = [
            ('file.someCrazyThing', 'unknown'),
            ('file.js',             'javascript'),
            ('file.Js',             'javascript'),
            ('file.JS',             'javascript'),
            ('file.awesome.js',     'javascript'),
            ('file.JavaScript',     'javascript')]
        for testFileName, expectedFileType in testFileNamesAndExpectedFileTypes:
            resource = Resource(testFileName)
            self.assertEqual(expectedFileType, resource.filetype, 'Expected "' + testFileName +
                '" to be detected as "' + expectedFileType + '"')

    def testResourceHasABaseNameProperty(self):
        testFileNamesAndExpectedBaseNames = [
            ('file.js', 'file'),
            ('FILE.JS', 'file'),
            ('some-Plugin-2.3.2-min.js', 'some-plugin'),
            ('jQuery-1.2.3.js', 'jquery')]
        for testFileName, expectedBaseName in testFileNamesAndExpectedBaseNames:
            resource = Resource(testFileName)
            self.assertEqual(expectedBaseName, resource.baseName, 'Expected the baseName of "' +
                testFileName + '" to be "'+ expectedBaseName + '" and not "' + resource.baseName + '"')