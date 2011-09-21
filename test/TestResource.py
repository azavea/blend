import unittest

from pipeline import Resource

class TestResource(unittest.TestCase):
    """Asserts that the properties and methods of the Resource class behave correctly."""

    def testResourceMustBeCreatedWithPathToFile(self):
        self.assertRaises(Exception, Resource)

    def testResourceMustBeCreatedWithAStringPathToFile(self):
        self.assertRaises(Exception, Resource, 1)

    def testResourceHasPathToFilePropertySetOnInit(self):
        testFileName = 'some/file/name.txt'
        resource = Resource(testFileName)
        self.assertEqual(testFileName, resource.pathToFile)

    def testResourceHasFileTypePropertyWithADefaultValueOfUnknown(self):
        testFileName = 'someFile'
        resource = Resource(testFileName)
        self.assertEqual('unknown', resource.filetype)

    def testResourceHasAnExtensionProperty(self):
        testFileNamesAndExpectedExtensions = [
            ('/var/someFile.js',            'js'),
            ('someFile.JS',            'js'),
            ('noExtension',            ''),
            ('someFile.SomECraZytype', 'somecrazytype')]
        for testFilePath, expectedExtension in testFileNamesAndExpectedExtensions:
            resource = Resource(testFilePath)
            self.assertEqual(expectedExtension, resource.extension, 'Expected the extension of "' +
                testFilePath + '" to be "' + expectedExtension + '"')

    def testResourceDetectsFileTypeByExtension(self):
        testFileNamesAndExpectedFileTypes = [
            ('file.someCrazyThing', 'unknown'),
            ('c:\\file.js',             'javascript'),
            ('file.Js',             'javascript'),
            ('file.JS',             'javascript'),
            ('file.awesome.js',     'javascript'),
            ('file.JavaScript',     'javascript')]
        for testFilePath, expectedFileType in testFileNamesAndExpectedFileTypes:
            resource = Resource(testFilePath)
            self.assertEqual(expectedFileType, resource.filetype, 'Expected "' + testFilePath +
                '" to be detected as "' + expectedFileType + '"')

    def testResourceHasABaseNameProperty(self):
        testFilePathsAndExpectedBaseNames = [
            ('/usr/local/file.js', 'file'),
            ('FILE.JS', 'file'),
            ('some-Plugin-2.3.2-min.js', 'some-plugin'),
            ('jQuery-1.2.3.js', 'jquery')]
        for testFilePath, expectedBaseName in testFilePathsAndExpectedBaseNames:
            resource = Resource(testFilePath)
            self.assertEqual(expectedBaseName, resource.baseName, 'Expected the baseName of "' +
                testFilePath + '" to be "'+ expectedBaseName + '" and not "' + resource.baseName + '"')