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
import sys
import subprocess
from distutils.core import setup, Command
import setuptools


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


class RunTests(Command):
    description = "Run the unit test suite for blend."
    user_options = []
    extra_env = {}
    extra_args = []

    def run(self):
        run_tests_script_path = os.path.join(os.path.dirname(__file__), 'blend', 'run_tests.py')
        sys.exit(subprocess.call([run_tests_script_path]))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

setup(
    name='Blend',
    version='0.1.1',
    author='Justin Walgran',
    author_email='jwalgran@azavea.com',
    packages=['blend', 'blend.test'],
    scripts=['bin/blend'],
    package_data={'blend': [
        'lib/js.jar',
        'lib/js_LICENSE.TXT',
        'lib/jslint.js',
        'lib/yuicompressor-2.4.6.jar',
        'lib/yuicompressor_LICENSE.TXT'
    ]},
    url='http://github.com/azavea/blend',
    license='LICENSE.txt',
    description='A cross-platform tool for merging and processing client-side assets for a web application.',
    long_description=read('README.rst'),
    cmdclass={'test': RunTests},
    keywords="javascript css html build",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Build Tools"
    ]
)
