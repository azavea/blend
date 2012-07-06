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

from blend import Result


class TestResult(unittest.TestCase):
    """Asserts that the properties and methods of the Result class behave correctly."""

    def setUp(self):
        self.result = Result()

    def tearDown(self):
        pass

    def test_adding_none_to_messages_does_not_create_a_message(self):
        self.result.add_message(None)
        self.result.add_warning("warning")
        self.result.add_error("error")
        self.assertIsNone(self.result.messages, "Expected adding a None message to not add an item to Result.messages")

    def test_adding_none_to_warnings_does_not_create_a_warning(self):
        self.result.add_message("message")
        self.result.add_warning(None)
        self.result.add_error("error")
        self.assertIsNone(self.result.warnings, "Expected adding a None warning to not add an item to Result.warnings")

    def test_adding_none_to_error_does_not_create_a_message(self):
        self.result.add_message("message")
        self.result.add_warning("warning")
        self.result.add_error(None)
        self.assertIsNone(self.result.errors, "Expected adding a None error to not add an item to Result.errors")

    def test_errors_warnings_and_messages_as_string_with_one_of_each(self):
        self.result.add_message("message")
        self.result.add_warning("warning")
        self.result.add_error("error")
        self.assertEqual("error\nwarning\nmessage", self.result.errors_warnings_and_messages_as_string)

    def test_errors_warnings_and_messages_as_string_with_message_and_warning(self):
        self.result.add_message("message")
        self.result.add_warning("warning")
        self.assertEqual("warning\nmessage", self.result.errors_warnings_and_messages_as_string)
