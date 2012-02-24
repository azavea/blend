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

import optparse
import os
import sys
import traceback
from Environment import Environment
from Resource import Resource

class Application():
    DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
    DEFAULT_ENV_PATH_LIST = []
    DEFAULT_INCLUDE_CWD = True
    DEFAULT_FILE_LIST = []

    def __init__(self, env_path_list=DEFAULT_ENV_PATH_LIST, include_cwd=DEFAULT_INCLUDE_CWD,
                 file_list=DEFAULT_FILE_LIST, output_dir=DEFAULT_OUTPUT_DIR):
        self.environment = Environment(*env_path_list, include_cwd=include_cwd)
        self.include_cwd = include_cwd
        self.file_list = file_list
        self.output_dir = output_dir

    def run(self):
        try:
            if len(self.file_list) == 0:
                resources = Resource.find_all_in_environment(self.environment)
            else:
                resources = []
                for file_path in self.file_list:
                    resources.append(Resource(file_path))
            if resources is not None:
                for resource in resources:
                    if resource.requirements is not None:
                        directory, file_name = os.path.split(resource.path_to_file)
                        merged_content = resource.merge_requirements_from_environment(self.environment, previously_merged=[])
                        if not os.path.exists(self.output_dir):
                            os.makedirs(self.output_dir)
                        f = open(os.path.join(self.output_dir, file_name), 'w')
                        try:
                            f.write(merged_content)
                        finally:
                            f.close()
        except Exception:
            traceback.print_exc(file=sys.stderr)
            return -1

        return 0

    @staticmethod
    def main():
        parser = optparse.OptionParser("""usage %prog [options] [file1 [file2 [fileN]]]

If no file arguments are specified, blend searches the specified
environment paths and processes any and all files that require other files.

If no environment paths are specified, the current working directory is
searched for required files.

If no output path is specified, an output directory is created in the
current working directory and all outputs are written to that directory.""")

        parser.add_option("-o", "--output",
            default=Application.DEFAULT_OUTPUT_DIR,
            dest='output_dir',
            metavar='OUTPUT',
            help="where the file output will be written")

        parser.add_option("-e", "--environment",
            default=Application.DEFAULT_ENV_PATH_LIST,
            dest='environment',
            metavar='ENV',
            action='append',
            help='a directory to be searched for required files (multiple directories can specified by repeating the flag)')

        parser.add_option("-s", "--skipcwd",
            default=not Application.DEFAULT_INCLUDE_CWD,
            dest='skip_cwd',
            metavar='ENV',
            action='store_true',
            help='exclude the current working directory from the environment')

        options, arguments = parser.parse_args()

        file_list = arguments or []

        app = Application(options.environment, not options.skip_cwd, file_list, options.output_dir)
        sys.exit(app.run())

if __name__ == '__main__':
    Application.main()