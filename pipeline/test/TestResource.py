import unittest
import tempfile

from pipeline import Resource, Environment
from pipeline.Requirement import RequirementNotSatisfiedException
from helpers import *

class TestResource(unittest.TestCase):
    """Asserts that the properties and methods of the Resource class behave correctly."""

    def setUp(self):
        self.test_env_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_env_dir)
        clean_output()

    def test_resource_must_be_created_with_path_to_file(self):
        self.assertRaises(Exception, Resource)

    def test_resource_must_be_created_with_a_non_none_path_to_file(self):
        self.assertRaises(Exception, Resource, None)

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
            ('/var/someFile.js',       'js'),
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
            ('/usr/local/file.js',       'file'),
            ('FILE.JS',                  'file'),
            ('some-Plugin-2.3.2-min.js', 'some-plugin'),
            ('jQuery-1.2.3.js',          'jquery')]
        for test_file_path, expected_base_name in test_file_paths_and_expected_base_names:
            resource = Resource(test_file_path)
            self.assertEqual(expected_base_name, resource.base_name, 'Expected the base_name of "' +
                test_file_path + '" to be "'+ expected_base_name + '" and not "' + resource.base_name + '"')

    def test_find_all_javascript_resources_in_the_default_environment(self):
        paths_to_test_files = [os.path.join(self.test_env_dir, 'test.js'), os.path.join(self.test_env_dir, 'test.css'),
            os.path.join(self.test_env_dir, 'test.html')]
        create_test_files(paths_to_test_files)
        resources = Resource.find_all_of_type_in_environment('javascript', Environment(self.test_env_dir))
        clean_up_test_files(paths_to_test_files)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')

    def test_find_all_javascript_resources_in_an_environment(self):
        paths_to_test_files = [os.path.join(self.test_env_dir, 'subdir', 'test.js'),
            os.path.join(self.test_env_dir, 'test.css'), os.path.join(self.test_env_dir, 'test.html')]
        test_env = Environment(self.test_env_dir, include_cwd=False)
        create_test_files(paths_to_test_files)
        resources = Resource.find_all_of_type_in_environment('javascript', test_env)
        clean_up_test_files(paths_to_test_files)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')
        self.assertEqual(os.path.join(self.test_env_dir, 'subdir', 'test.js'),
            resources[0].path_to_file)

    def test_search_for_javascript_resources_in_an_environment_without_any_returns_none(self):
        test_env = Environment(self.test_env_dir, include_cwd=False)
        path_to_test_file = os.path.join(self.test_env_dir, 'test.css')
        create_test_files(path_to_test_file)
        resources = Resource.find_all_of_type_in_environment('javascript', test_env)
        self.assertEquals(None, resources)

    def test_exists_property(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.js')
        clean_up_test_files(path_to_test_file)
        resource = Resource(path_to_test_file)
        # file does not exist yet
        self.assertFalse(resource.exists)
        create_test_files(path_to_test_file)
        self.assertTrue(resource.exists)
        clean_up_test_files(path_to_test_file)

    def test_content_property(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.js')
        content = 'var foo = {};'
        create_test_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertEquals(content, resource.content)
        clean_up_test_files(path_to_test_file)

    def test_requirements_property_for_resource_without_content_is_none(self):
        resource = Resource('some file')
        self.assertTrue(resource.content is None)
        self.assertEqual(None, resource.requirements)

    def test_requirements_property_for_resource_with_plain_content_is_none(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.js')
        clean_up_test_files(path_to_test_file)
        content = 'var foo = {};'
        create_test_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(None, resource.requirements)
        clean_up_test_files(path_to_test_file)

    def test_javascript_requirements_are_found(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.js')
        clean_up_test_files(path_to_test_file)
        content = '//= require <jquery>\nvar foo = {};//= require "openlayers"\n var s = "some other thing"\n'
        create_test_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(2, len(resource.requirements))
        self.assertEqual('jquery', resource.requirements[0].name)
        self.assertEqual('global', resource.requirements[0].type)
        self.assertEqual((0,21), resource.requirements[0].insert_location)
        self.assertEqual('openlayers', resource.requirements[1].name)
        self.assertEqual('local', resource.requirements[1].type)
        self.assertEqual((34,59), resource.requirements[1].insert_location)
        clean_up_test_files(path_to_test_file)

    def test_css_import_statements_found_as_requirements(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.css')
        clean_up_test_files(path_to_test_file)
        content = 'h1 {background:red;}\n @import url("something.css")'
        create_test_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(1, len(resource.requirements))
        self.assertEqual('something', resource.requirements[0].name)
        self.assertEqual('local', resource.requirements[0].type)
        self.assertEqual((22,50), resource.requirements[0].insert_location)

    def test_css_require_comments_found_as_requirements(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.css')
        clean_up_test_files(path_to_test_file)
        content = 'h1 {background:red;}\n /*= require "something"  */'
        create_test_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(1, len(resource.requirements))
        self.assertEqual('something', resource.requirements[0].name)
        self.assertEqual('local', resource.requirements[0].type)
        self.assertEqual((21,49), resource.requirements[0].insert_location)

    def test_merge_requirements_in_global_path(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.js')]
        clean_up_test_files(paths_to_test_files)
        create_test_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require <FILE2>')
        create_test_file_with_content(paths_to_test_files[1], '// This is file 2')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_environment(Environment(self.test_env_dir,
            include_cwd=False), previously_merged=[])

        self.assertEqual('// This is file 1\n// This is file 2', actual_merged_content)

        clean_up_test_files(paths_to_test_files)

    def test_merge_js_requirements_in_local_path(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir1', 'file2.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.js')]
        clean_up_test_files(paths_to_test_files)
        create_test_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require "FILE2"')
        create_test_file_with_content(paths_to_test_files[1], '// This is LOCAL file 2')
        create_test_file_with_content(paths_to_test_files[2], '// This is GLOBAL file 2')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_environment(Environment(self.test_env_dir,
                                                                                               include_cwd=False), previously_merged=[])

        self.assertEqual('// This is file 1\n// This is LOCAL file 2', actual_merged_content)

        clean_up_test_files(paths_to_test_files)

    def test_merge_css_requirements_in_local_path(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.css'),
            os.path.join(self.test_env_dir, 'dir1', 'file2.css'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.css')]
        clean_up_test_files(paths_to_test_files)
        create_test_file_with_content(paths_to_test_files[0], '/* This is file 1 */\n@import url("FiLe2.css")')
        create_test_file_with_content(paths_to_test_files[1], '/* This is LOCAL file 2 */')
        create_test_file_with_content(paths_to_test_files[2], '/* This is GLOBAL file 2 */')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_environment(Environment(self.test_env_dir,
                                                                                               include_cwd=False), previously_merged=[])

        self.assertEqual('/* This is file 1 */\n/* This is LOCAL file 2 */', actual_merged_content)

        clean_up_test_files(paths_to_test_files)

    def test_global_resource_not_merged_for_local_requirement(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.js')]
        clean_up_test_files(paths_to_test_files)
        create_test_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require "FILE2"')
        create_test_file_with_content(paths_to_test_files[1], '// This is GLOBAL file 2')
        file1_resource = Resource(paths_to_test_files[0])

        self.assertRaises(RequirementNotSatisfiedException, file1_resource.merge_requirements_from_environment,
            Environment(self.test_env_dir, include_cwd=False), previously_merged=[])

    def test_merge_recursive_requirements_in_global_path(self):
        paths_to_test_files = [
                os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
                os.path.join(self.test_env_dir, 'dir2', 'file2.js'),
                os.path.join(self.test_env_dir, 'dir3', 'file3.js')]
        clean_up_test_files(paths_to_test_files)
        create_test_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require <FILE2>')
        create_test_file_with_content(paths_to_test_files[1], '// This is file 2\n//= require <file3>')
        create_test_file_with_content(paths_to_test_files[2], '// This is file 3')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_environment(Environment(self.test_env_dir, include_cwd=False), previously_merged=[])
        self.assertEqual('// This is file 1\n// This is file 2\n// This is file 3', actual_merged_content)
        clean_up_test_files(paths_to_test_files)

    def test_merge_from_global_path_does_not_add_requirements_twice(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir11', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir21', 'file2.js'),
            os.path.join(self.test_env_dir, 'dir31', 'file3.js'),
            os.path.join(self.test_env_dir, 'dir41', 'file4.js')]
        clean_up_test_files(paths_to_test_files)
        create_test_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require <file2>\n//= require <file3>')
        create_test_file_with_content(paths_to_test_files[1], '// This is file 2\n//= require <file4>')
        create_test_file_with_content(paths_to_test_files[2], '// This is file 3\n//= require <file4>')
        create_test_file_with_content(paths_to_test_files[3], '// This is file 4\n')

        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_environment(Environment(self.test_env_dir, include_cwd=False), previously_merged=[])
        self.assertEqual('// This is file 1\n// This is file 2\n// This is file 3\n// This is file 4\n', actual_merged_content)
        clean_up_test_files(paths_to_test_files)

    def test_find_all_in_environment(self):
        paths_to_processable_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.css')]

        paths_to_unprocessable_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'movie.avi'),
            os.path.join(self.test_env_dir, 'some.other.thing')]

        create_test_files(paths_to_processable_test_files)
        create_test_files(paths_to_unprocessable_test_files)

        resources = Resource.find_all_in_environment(Environment(self.test_env_dir, include_cwd=False))

        self.assertEquals(2, len(resources))
        self.assertEqual(paths_to_processable_test_files[0], resources[0].path_to_file)
        self.assertEqual(paths_to_processable_test_files[1], resources[1].path_to_file)