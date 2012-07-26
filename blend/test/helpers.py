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

import os
import shutil


def create_files(paths_to_files):
    if isinstance(paths_to_files, basestring):
        internal_paths_to_files = [paths_to_files]
    else:
        internal_paths_to_files = paths_to_files
    for path_to_file in internal_paths_to_files:
        if not os.path.exists(path_to_file):
            if os.path.dirname(path_to_file) != '' and not os.path.exists(os.path.dirname(path_to_file)):
                os.makedirs(os.path.dirname(path_to_file))
            open(path_to_file, 'w').close()


def create_file_with_content(path_to_test_file, content):
    create_files(path_to_test_file)
    f = open(path_to_test_file, 'w')
    try:
        f.write(content)
    finally:
        f.close()


def clean_up_files(paths_to_files):
    if isinstance(paths_to_files, basestring):
        internal_paths_to_files = [paths_to_files]
    else:
        internal_paths_to_files = paths_to_files
    for path_to_file in internal_paths_to_files:
        if os.path.exists(path_to_file):
            os.remove(path_to_file)


def clean_output():
    output_dir = os.path.join(os.getcwd(), "output")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
