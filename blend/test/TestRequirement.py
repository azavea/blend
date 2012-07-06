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

from blend import Requirement


class TestRequirement(unittest.TestCase):

    def test_requirement_must_be_created_with_a_name(self):
        self.assertRaises(Exception, Requirement)
        self.assertRaises(Exception, Requirement, None)
        requirement = Requirement('name')
        self.assertEqual('name', requirement.name)

    def test_requirement_name_must_be_a_string(self):
        self.assertRaises(Exception, Requirement, 1)

    def test_requirement_has_a_default_insert_location(self):
        requirement = Requirement('name')
        self.assertEqual(0, requirement.insert_location)

    def test_requirement_takes_insert_location_as_an_optional_parameter(self):
        requirement = Requirement('name', 1)
        self.assertEqual(1, requirement.insert_location)
        requirement = Requirement('name', (10, 22))
        self.assertEqual((10, 22), requirement.insert_location)

    def test_insert_location_must_not_be_a_string(self):
        self.assertRaises(Exception, Requirement, 'name', 'some string')
