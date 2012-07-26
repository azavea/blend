# By Justin Walgran
# Copyright (c) 2012 Azavea, Inc.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import unittest
import tempfile

from blend import Resource, Paths
import shutil
import os
import helpers


class TestResource(unittest.TestCase):
    """Asserts that the properties and methods of the Resource class behave correctly."""

    def setUp(self):
        self.test_env_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_env_dir)
        helpers.clean_output()

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

    def test_resource_has_a_size_property(self):
        test_env_dir = tempfile.mkdtemp()
        test_file_path = os.path.join(test_env_dir, 'test_file.txt')
        helpers.create_file_with_content(test_file_path, 'some\ttext\non two lines')
        resource = Resource(test_file_path)
        self.assertEqual(22, resource.size)
        shutil.rmtree(test_env_dir)

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
                test_file_path + '" to be "' + expected_base_name + '" and not "' + resource.base_name + '"')

    def test_find_all_javascript_resources_in_the_paths(self):
        paths_to_test_files = [os.path.join(self.test_env_dir, 'test.js'), os.path.join(self.test_env_dir, 'test.css'),
            os.path.join(self.test_env_dir, 'test.html')]
        helpers.create_files(paths_to_test_files)
        resources = Resource.find_all_of_type_in_paths('javascript', Paths(self.test_env_dir, include_cwd=False))
        helpers.clean_up_files(paths_to_test_files)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')

    def test_find_all_javascript_resources_in_paths(self):
        paths_to_test_files = [os.path.join(self.test_env_dir, 'subdir', 'test.js'),
            os.path.join(self.test_env_dir, 'test.css'), os.path.join(self.test_env_dir, 'test.html')]
        test_env = Paths(self.test_env_dir, include_cwd=False)
        helpers.create_files(paths_to_test_files)
        resources = Resource.find_all_of_type_in_paths('javascript', test_env)
        helpers.clean_up_files(paths_to_test_files)
        self.assertEquals(1, len(resources), 'One and only one javascript file should be found')
        self.assertEqual(os.path.join(self.test_env_dir, 'subdir', 'test.js'),
            resources[0].path_to_file)

    def test_search_for_javascript_resources_in_paths_without_any_search_paths_returns_none(self):
        test_env = Paths(self.test_env_dir, include_cwd=False)
        path_to_test_file = os.path.join(self.test_env_dir, 'test.css')
        helpers.create_files(path_to_test_file)
        resources = Resource.find_all_of_type_in_paths('javascript', test_env)
        self.assertEquals(None, resources)

    def test_exists_property(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.js')
        helpers.clean_up_files(path_to_test_file)
        resource = Resource(path_to_test_file)
        # file does not exist yet
        self.assertFalse(resource.exists)
        helpers.create_files(path_to_test_file)
        self.assertTrue(resource.exists)
        helpers.clean_up_files(path_to_test_file)

    def test_content_property(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.js')
        content = 'var foo = {};'
        helpers.create_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertEquals(content, resource.content)
        helpers.clean_up_files(path_to_test_file)

    def test_requirements_property_for_resource_without_content_is_none(self):
        resource = Resource('some file')
        self.assertTrue(resource.content is None)
        self.assertEqual(None, resource.requirements)

    def test_requirements_property_for_resource_with_plain_content_is_none(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.js')
        helpers.clean_up_files(path_to_test_file)
        content = 'var foo = {};'
        helpers.create_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(None, resource.requirements)
        helpers.clean_up_files(path_to_test_file)

    def test_javascript_requirements_are_found(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.js')
        helpers.clean_up_files(path_to_test_file)
        content = '//= require jquery\nvar foo = {};//= require openlayers\n var s = some other thing\n'
        helpers.create_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(2, len(resource.requirements))
        self.assertEqual('jquery', resource.requirements[0].name)
        self.assertEqual((0, 19), resource.requirements[0].insert_location)
        self.assertEqual('openlayers', resource.requirements[1].name)
        self.assertEqual((32, 55), resource.requirements[1].insert_location)
        helpers.clean_up_files(path_to_test_file)

    def test_css_import_statements_found_as_requirements(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.css')
        helpers.clean_up_files(path_to_test_file)
        content = 'h1 {background:red;}\n @import url("something.css")'
        helpers.create_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(1, len(resource.requirements))
        self.assertEqual('something', resource.requirements[0].name)
        self.assertEqual((22, 50), resource.requirements[0].insert_location)

    def test_css_require_comments_found_as_requirements(self):
        path_to_test_file = os.path.join(self.test_env_dir, 'test.css')
        helpers.clean_up_files(path_to_test_file)
        content = 'h1 {background:red;}\n /*= require something  */'
        helpers.create_file_with_content(path_to_test_file, content)
        resource = Resource(path_to_test_file)
        self.assertTrue(resource.content == content)
        self.assertEqual(1, len(resource.requirements))
        self.assertEqual('something', resource.requirements[0].name)
        self.assertEqual((21, 47), resource.requirements[0].insert_location)

    def test_merge_requirements_in_global_path(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.js')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require FILE2')
        helpers.create_file_with_content(paths_to_test_files[1], '// This is file 2')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir,
            include_cwd=False), previously_merged=[])

        self.assertEqual('// This is file 1\n// This is file 2', actual_merged_content)

        helpers.clean_up_files(paths_to_test_files)

    def test_merge_js_requirements_in_local_path(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir1', 'file2.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.js')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require FILE2')
        helpers.create_file_with_content(paths_to_test_files[1], '// This is LOCAL file 2')
        helpers.create_file_with_content(paths_to_test_files[2], '// This is GLOBAL file 2')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir,
                                                                                               include_cwd=False), previously_merged=[])

        self.assertEqual('// This is file 1\n// This is LOCAL file 2', actual_merged_content)

        helpers.clean_up_files(paths_to_test_files)

    def test_merge_js_requirements_favors_closer_files(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir1', 'file2.js'),
            os.path.join(self.test_env_dir, 'dir1', 'dir2', 'file2.js')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require FILE2')
        helpers.create_file_with_content(paths_to_test_files[1], '// This is NEARBY file 2')
        helpers.create_file_with_content(paths_to_test_files[2], '// This is FAR AWAY file 2')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir,
            include_cwd=False), previously_merged=[])

        self.assertEqual('// This is file 1\n// This is NEARBY file 2', actual_merged_content)

    def test_merge_js_requirements_favors_downward_matches(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'dir2', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir1', 'file2.js'),
            os.path.join(self.test_env_dir, 'dir1', 'dir2', 'dir3', 'file2.js')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require FILE2')
        helpers.create_file_with_content(paths_to_test_files[1], '// This is UPWARD file 2')
        helpers.create_file_with_content(paths_to_test_files[2], '// This is DOWNWARD file 2')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir,
            include_cwd=False), previously_merged=[])

        self.assertEqual('// This is file 1\n// This is DOWNWARD file 2', actual_merged_content)

    def test_merge_js_requirements_favors_shallow_downward_matches(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir1', 'dir2', 'file2.js'),
            os.path.join(self.test_env_dir, 'dir1', 'dir2', 'dir3', 'file2.js')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require FILE2')
        helpers.create_file_with_content(paths_to_test_files[1], '// This is SHALLOW file 2')
        helpers.create_file_with_content(paths_to_test_files[2], '// This is DEEP file 2')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir,
            include_cwd=False), previously_merged=[])

        self.assertEqual('// This is file 1\n// This is SHALLOW file 2', actual_merged_content)

    def test_merge_js_requirements_favors_shallow_upward_matches(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'dir2', 'dir3', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir1', 'dir2', 'file2.js'),
            os.path.join(self.test_env_dir, 'dir1', 'file2.js')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require FILE2')
        helpers.create_file_with_content(paths_to_test_files[1], '// This is NEAR file 2')
        helpers.create_file_with_content(paths_to_test_files[2], '// This is FAR file 2')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir,
            include_cwd=False), previously_merged=[])
        self.assertEqual('// This is file 1\n// This is NEAR file 2', actual_merged_content)

    def test_merge_css_requirements_in_local_path(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.css'),
            os.path.join(self.test_env_dir, 'dir1', 'file2.css'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.css')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '/* This is file 1 */\n@import url("FiLe2.css")')
        helpers.create_file_with_content(paths_to_test_files[1], '/* This is LOCAL file 2 */')
        helpers.create_file_with_content(paths_to_test_files[2], '/* This is GLOBAL file 2 */')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir,
                                                                                               include_cwd=False), previously_merged=[])

        self.assertEqual('/* This is file 1 */\n/* This is LOCAL file 2 */', actual_merged_content)

        helpers.clean_up_files(paths_to_test_files)

    def test_merge_recursive_requirements_in_global_path(self):
        paths_to_test_files = [
                os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
                os.path.join(self.test_env_dir, 'dir2', 'file2.js'),
                os.path.join(self.test_env_dir, 'dir3', 'file3.js')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require FILE2')
        helpers.create_file_with_content(paths_to_test_files[1], '// This is file 2\n//= require file3')
        helpers.create_file_with_content(paths_to_test_files[2], '// This is file 3')
        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir, include_cwd=False), previously_merged=[])
        self.assertEqual('// This is file 1\n// This is file 2\n// This is file 3', actual_merged_content)
        helpers.clean_up_files(paths_to_test_files)

    def test_merge_from_global_path_does_not_add_requirements_twice(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir11', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir21', 'file2.js'),
            os.path.join(self.test_env_dir, 'dir31', 'file3.js'),
            os.path.join(self.test_env_dir, 'dir41', 'file4.js')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '// This is file 1\n//= require file2\n//= require file3')
        helpers.create_file_with_content(paths_to_test_files[1], '// This is file 2\n//= require file4')
        helpers.create_file_with_content(paths_to_test_files[2], '// This is file 3\n//= require file4')
        helpers.create_file_with_content(paths_to_test_files[3], '// This is file 4\n')

        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir, include_cwd=False), previously_merged=[])
        self.assertEqual('// This is file 1\n// This is file 2\n// This is file 4\n// This is file 3\n', actual_merged_content)
        helpers.clean_up_files(paths_to_test_files)

    def test_merge_library_required_at_the_top_of_multiple_files(self):
        paths_to_test_files = [
            os.path.join(self.test_env_dir, 'dir11', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir21', 'file2.js'),
            os.path.join(self.test_env_dir, 'dir31', 'file3.js'),
            os.path.join(self.test_env_dir, 'dir41', 'file4.js')]
        helpers.clean_up_files(paths_to_test_files)
        helpers.create_file_with_content(paths_to_test_files[0], '//= require file2\n//= require file3\n// This is file 1\n')
        helpers.create_file_with_content(paths_to_test_files[1], '//= require file4\n// This is file 2\n')
        helpers.create_file_with_content(paths_to_test_files[2], '//= require file4\n// This is file 3\n')
        helpers.create_file_with_content(paths_to_test_files[3], '// This is file 4\n')

        file1_resource = Resource(paths_to_test_files[0])
        actual_merged_content = file1_resource.merge_requirements_from_paths(Paths(self.test_env_dir, include_cwd=False), previously_merged=[])
        self.assertEqual('// This is file 4\n// This is file 2\n// This is file 3\n// This is file 1\n', actual_merged_content)
        helpers.clean_up_files(paths_to_test_files)

    def test_find_all_in_paths(self):
        paths_to_processable_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file2.css')]

        paths_to_unprocessable_test_files = [
            os.path.join(self.test_env_dir, 'dir1', 'movie.avi'),
            os.path.join(self.test_env_dir, 'some.other.thing')]

        helpers.create_files(paths_to_processable_test_files)
        helpers.create_files(paths_to_unprocessable_test_files)

        resources = Resource.find_all_in_paths(Paths(self.test_env_dir, include_cwd=False))

        self.assertEquals(2, len(resources))
        self.assertEqual(paths_to_processable_test_files[0], resources[0].path_to_file)
        self.assertEqual(paths_to_processable_test_files[1], resources[1].path_to_file)

    def test_detects_minification_from_file_name(self):
        test_file_paths = [
            os.path.join(self.test_env_dir, 'dir1', 'file1.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file1.min.js'),
            os.path.join(self.test_env_dir, 'dir2', 'file1-min.js')]

        helpers.create_files(test_file_paths)

        unminified_resource = Resource(test_file_paths[0])
        minified_resource_with_dot = Resource(test_file_paths[1])
        minified_resource_with_dash = Resource(test_file_paths[2])

        self.assertFalse(unminified_resource.minified)
        self.assertTrue(minified_resource_with_dot.minified)
        self.assertTrue(minified_resource_with_dash.minified)
