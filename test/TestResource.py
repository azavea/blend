import unittest
import os

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

    def testFindAllJavascriptResources(self):
        pathsToTestFiles = ['test.js', 'test.css', 'test.html']
        TestResource.createTestFiles(pathsToTestFiles)
        resources = Resource.findAllOfType('javascript')
        TestResource.cleanUpTestFiles(pathsToTestFiles)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')

    def testFindAllJavascriptResourcesInAPath(self):
        pathsToTestFiles = ['/tmp/subdir/test.js', '/tmp/test.css', '/tmp/test.html']
        TestResource.createTestFiles(pathsToTestFiles)
        resources = Resource.findAllOfTypeInPath('javascript', '/tmp')
        TestResource.cleanUpTestFiles(pathsToTestFiles)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')

    def testExistsProperty(self):
        pathsToTestFiles = ['/tmp/test.js']
        resource = Resource(pathsToTestFiles[0])
        # file does not exist yet
        self.assertFalse(resource.exists)
        TestResource.createTestFiles(pathsToTestFiles)
        self.assertTrue(resource.exists)
        TestResource.cleanUpTestFiles(pathsToTestFiles)

    def testContentProperty(self):
        pathsToTestFiles = ['/tmp/test.js']
        content = 'var foo = {};'
        TestResource.createTestFiles(pathsToTestFiles)
        f = open(pathsToTestFiles[0], 'w')
        f.write(content)
        f.close()
        resource = Resource(pathsToTestFiles[0])
        self.assertEquals(content, resource.content)
        TestResource.cleanUpTestFiles(pathsToTestFiles)

    @staticmethod
    def createTestFiles(pathsToFiles):
        for pathToFile in pathsToFiles:
            if not os.path.exists(pathToFile):
                if os.path.dirname(pathToFile) != '' and not os.path.exists(os.path.dirname(pathToFile)):
                    os.makedirs(os.path.dirname(pathToFile))
                open(pathToFile, 'w').close()

    @staticmethod
    def cleanUpTestFiles(pathsToFiles):
        for pathToFile in pathsToFiles:
            if os.path.exists(pathToFile):
                os.remove(pathToFile)