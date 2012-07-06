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
from blend import Minification


class TestMinification(unittest.TestCase):

    def setUp(self):
        self.minification = Minification()

    def tearDown(self):
        pass

    def test_has_a_content_property(self):
        self.assertIsNone(self.minification.content)

    def test_can_set_content(self):
        self.minification.set_content("content")
        self.assertEqual("content", self.minification.content)

    def test_converting_a_good_minification_to_string_returns_content(self):
        self.minification.mark_as_good()
        self.minification.set_content("content")
        self.assertEqual("content", str(self.minification))

    def test_converting_a_bad_minification_to_string_returns_error(self):
        self.minification.mark_as_bad()
        self.minification.set_content("content")
        self.minification.add_error("error message")
        self.assertEqual("error message", str(self.minification))
