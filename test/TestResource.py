import unittest
import os
import shutil

from pipeline import Resource, Environment

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
            ('c:\\file.js',         'javascript'),
            ('file.Js',             'javascript'),
            ('file.JS',             'javascript'),
            ('file.awesome.js',     'javascript'),
            ('file.JavaScript',     'javascript'),
            ('file.css',            'css'),
            ('FILE.CSS',            'css')]
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

    def test_find_all_javascript_resources_in_the_default_environment(self):
        paths_to_test_files = ['test.js', 'test.css', 'test.html']
        TestResource.create_test_files(paths_to_test_files)
        resources = Resource.find_all_of_type_in_environment('javascript', Environment())
        TestResource.clean_up_test_files(paths_to_test_files)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')

    def test_find_all_javascript_resources_in_an_environment(self):
        paths_to_test_files = ['/tmp/subdir/test.js', '/tmp/test.css', '/tmp/test.html']
        test_env = Environment('/tmp', include_cwd=False)
        TestResource.create_test_files(paths_to_test_files)
        resources = Resource.find_all_of_type_in_environment('javascript', test_env)
        TestResource.clean_up_test_files(paths_to_test_files)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')
        self.assertEqual(os.path.join('/','tmp','subdir', 'test.js'), resources[0].path_to_file)

    def test_search_for_javascript_resources_in_an_environment_without_any_returns_none(self):
        test_dir = '/tmp/only_css'
        test_env = Environment(test_dir, include_cwd=False)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        path_to_test_file = '/tmp/only_css/test.css'
        TestResource.create_test_files(path_to_test_file)
        resources = Resource.find_all_of_type_in_environment('javascript', test_env)
        self.assertEquals(None, resources)

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
        TestResource.create_test_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertEquals(content, resource.content)
        TestResource.clean_up_test_files(path_to_test_file)

    def test_requirements_property_for_resource_without_content_is_none(self):
        resource = Resource('some file')
        self.assertTrue(resource.content is None)
        self.assertEqual(None, resource.requirements)

    def test_requirements_property_for_resource_with_plain_content_is_none(self):
        path_to_test_file = '/tmp/test.js'
        TestResource.clean_up_test_files(path_to_test_file)
        content = 'var foo = {};'
        TestResource.create_test_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(None, resource.requirements)
        TestResource.clean_up_test_files(path_to_test_file)

    def test_javascript_requirements_are_found(self):
        path_to_test_file = '/tmp/test.js'
        TestResource.clean_up_test_files(path_to_test_file)
        content = '//= require <jquery>\nvar foo = {};//= require "openlayers"\n var s = "some other thing"\n'
        TestResource.create_test_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(2, len(resource.requirements))
        self.assertEqual('jquery', resource.requirements[0].name)
        self.assertEqual('global', resource.requirements[0].type)
        self.assertEqual((0,20), resource.requirements[0].insert_location)
        self.assertEqual('openlayers', resource.requirements[1].name)
        self.assertEqual('local', resource.requirements[1].type)
        self.assertEqual((34,58), resource.requirements[1].insert_location)
        TestResource.clean_up_test_files(path_to_test_file)

    def test_css_import_statements_found_as_requirements(self):
        path_to_test_file = '/tmp/test.css'
        TestResource.clean_up_test_files(path_to_test_file)
        content = 'h1 {background:red;}\n @import url("something.css")'
        TestResource.create_test_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(1, len(resource.requirements))
        self.assertEqual('something.css', resource.requirements[0].name)
        self.assertEqual('local', resource.requirements[0].type)
        self.assertEqual((22,50), resource.requirements[0].insert_location)

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
    def create_test_file_with_content(path_to_test_file, content):
        TestResource.create_test_files(path_to_test_file)
        f = open(path_to_test_file, 'w')
        try:
            f.write(content)
        finally:
            f.close()

    @staticmethod
    def clean_up_test_files(paths_to_files):
        if isinstance(paths_to_files, basestring):
            internal_paths_to_files = [paths_to_files]
        else:
            internal_paths_to_files = paths_to_files
        for path_to_file in internal_paths_to_files:
            if os.path.exists(path_to_file):
                os.remove(path_to_file)