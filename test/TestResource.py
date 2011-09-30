import unittest
import os

from pipeline import Resource

class TestResource(unittest.TestCase):
    """Asserts that the properties and methods of the Resource class behave correctly."""

    def test_resource_must_be_created_with_path_to_file(self):
        self.assertRaises(Exception, Resource)

    def test_resource_must_be_created_with_a_string_argument(self):
        self.assertRaises(Exception, Resource, 1)

    def test_resource_has_path_to_file_property_set_on_instantiation(self):
        test_file_name = 'some/file/name.txt'
        resource = Resource(test_file_name)
        self.assertEqual(test_file_name, resource.path_to_file)

    def test_resource_has_a_file_type_property_with_a_default_value_of_unknown(self):
        test_file_name = 'someFile'
        resource = Resource(test_file_name)
        self.assertEqual('unknown', resource.file_type)

    def test_resource_has_an_extension_property(self):
        test_file_names_and_expected_extensions = [
            ('/var/someFile.js',            'js'),
            ('someFile.JS',            'js'),
            ('noExtension',            ''),
            ('someFile.SomECraZytype', 'somecrazytype')]
        for test_file_path, expected_extension in test_file_names_and_expected_extensions:
            resource = Resource(test_file_path)
            self.assertEqual(expected_extension, resource.extension, 'Expected the extension of "' +
                test_file_path + '" to be "' + expected_extension + '"')

    def test_resource_detects_file_type_by_extension(self):
        test_file_paths_and_expected_file_types = [
            ('file.someCrazyThing', 'unknown'),
            ('c:\\file.js',             'javascript'),
            ('file.Js',             'javascript'),
            ('file.JS',             'javascript'),
            ('file.awesome.js',     'javascript'),
            ('file.JavaScript',     'javascript')]
        for test_file_path, expected_file_type in test_file_paths_and_expected_file_types:
            resource = Resource(test_file_path)
            self.assertEqual(expected_file_type, resource.file_type, 'Expected "' + test_file_path +
                '" to be detected as "' + expected_file_type + '"')

    def test_resource_has_a_base_name_property(self):
        test_file_paths_and_expected_base_names = [
            ('/usr/local/file.js', 'file'),
            ('FILE.JS', 'file'),
            ('some-Plugin-2.3.2-min.js', 'some-plugin'),
            ('jQuery-1.2.3.js', 'jquery')]
        for test_file_path, expected_base_name in test_file_paths_and_expected_base_names:
            resource = Resource(test_file_path)
            self.assertEqual(expected_base_name, resource.base_name, 'Expected the base_name of "' +
                test_file_path + '" to be "'+ expected_base_name + '" and not "' + resource.base_name + '"')

    def test_find_all_javascript_resources(self):
        paths_to_test_files = ['test.js', 'test.css', 'test.html']
        TestResource.create_test_files(paths_to_test_files)
        resources = Resource.find_all_of_type('javascript')
        TestResource.clean_up_test_files(paths_to_test_files)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')

    def test_find_all_javascript_resources_in_a_path(self):
        paths_to_test_files = ['/tmp/subdir/test.js', '/tmp/test.css', '/tmp/test.html']
        TestResource.create_test_files(paths_to_test_files)
        resources = Resource.find_all_of_type_in_path('javascript', '/tmp')
        TestResource.clean_up_test_files(paths_to_test_files)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')

    def test_exists_property(self):
        path_to_test_file = '/tmp/test.js'
        TestResource.clean_up_test_files(path_to_test_file)
        resource = Resource(path_to_test_file)
        # file does not exist yet
        self.assertFalse(resource.exists)
        TestResource.create_test_files(path_to_test_file)
        self.assertTrue(resource.exists)
        TestResource.clean_up_test_files(path_to_test_file)

    def test_content_property(self):
        path_to_test_file = '/tmp/test.js'
        content = 'var foo = {};'
        TestResource.create_test_files(path_to_test_file)
        f = open(path_to_test_file, 'w')
        f.write(content)
        f.close()
        resource = Resource(path_to_test_file)
        self.assertEquals(content, resource.content)
        TestResource.clean_up_test_files(path_to_test_file)

    @staticmethod
    def create_test_files(paths_to_files):
        if isinstance(paths_to_files, basestring):
            internal_paths_to_files = [paths_to_files]
        else:
            internal_paths_to_files = paths_to_files
        for path_to_file in internal_paths_to_files:
            if not os.path.exists(path_to_file):
                if os.path.dirname(path_to_file) != '' and not os.path.exists(os.path.dirname(path_to_file)):
                    os.makedirs(os.path.dirname(path_to_file))
                open(path_to_file, 'w').close()

    @staticmethod
    def clean_up_test_files(paths_to_files):
        if isinstance(paths_to_files, basestring):
            internal_paths_to_files = [paths_to_files]
        else:
            internal_paths_to_files = paths_to_files
        for path_to_file in internal_paths_to_files:
            if os.path.exists(path_to_file):
                os.remove(path_to_file)