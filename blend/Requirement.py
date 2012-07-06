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


class Requirement:
    """
    Represents the a dependency that one Resource has on another.
    """
    def __init__(self, name, insert_location=0):
        """
        Arguments:
        name -- The string name of the required resource
        insert_location -- The character position within the content where the required
        resource will be inserted during a merge. Can be either a single integer for
        inserting without replacement or a tuple defining the character range in the
        requiring resource that will be replaced by the content of the required resource.
        """
        if not name:
            raise Exception('Requirement must be created with a name')
        if not isinstance(name, str):
            raise Exception('The name argument must be set to a string')
        self._name = name

        if isinstance(insert_location, basestring):
            raise Exception('The insert_location argument must be a number or a two-number tuple')
        self._insert_location = insert_location

    @property
    def name(self):
        """
        The string name of the required resource
        """
        return self._name

    @property
    def standard_name(self):
        """
        The lowercase name of the required resource
        """
        return self._name.lower()

    @property
    def insert_location(self):
        """
        The character position within the content where the required resource will be
        inserted during a merge. Can be either a single integer for inserting without
        replacement or a tuple defining the character range in the requiring resource
        that will be replaced by the content of the required resource.
        """
        return self._insert_location


class RequirementNotSatisfiedException(Exception):
    def __init__(self, requirement, paths, *args, **kwargs):
        super(RequirementNotSatisfiedException, self).__init__(*args, **kwargs)
        self.requirement = requirement
        self.paths = paths

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "Requirement:\n\t%s\nSearch paths:\n\t%s" % (self.requirement.name, '\n\t'.join(self.paths.search_paths))
