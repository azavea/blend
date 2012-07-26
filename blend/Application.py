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
from Paths import Paths
from Resource import Resource
from Configuration import Configuration
from JSLintAnalyzer import JSLintAnalyzer
from YUICompressorMinifier import YUICompressorMinifier
from blend.Requirement import RequirementNotSatisfiedException


class Application():
    DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
    DEFAULT_PATH_LIST = []
    DEFAULT_INCLUDE_CWD = True
    DEFAULT_FILE_LIST = []
    DEFAULT_CONFIG_FILE_PATH = os.path.join(os.getcwd(), '.blend', 'config.json')

    def __init__(self, path_list=DEFAULT_PATH_LIST, include_cwd=DEFAULT_INCLUDE_CWD,
                 file_list=DEFAULT_FILE_LIST, output_dir=DEFAULT_OUTPUT_DIR, config_file_path=DEFAULT_CONFIG_FILE_PATH):
        self.paths = Paths(*path_list, include_cwd=include_cwd)
        self.include_cwd = include_cwd
        self.file_list = file_list
        self.output_dir = output_dir
        if os.path.exists(config_file_path):
            print config_file_path
            self.config = Configuration(config_file_path)
        else:
            self.config = self._create_default_configuration()

    def _create_default_configuration(self):
        config = Configuration()
        config.add_analyzer_for_file_type(JSLintAnalyzer(), 'javascript', [os.path.join('lib', '*')])
        config.set_minifier_for_file_type(YUICompressorMinifier(), 'javascript')
        config.set_minifier_for_file_type(YUICompressorMinifier(), 'css')
        return config

    def run(self):
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            if len(self.file_list) == 0:
                resources = Resource.find_all_in_paths(self.paths)
            else:
                resources = []
                for file_path in self.file_list:
                    resources.append(Resource(file_path))
            if resources is not None:
                for resource in resources:
                    if resource.requirements is not None:
                        directory, file_name = os.path.split(resource.path_to_file)

                        try:
                            chunks = resource.get_chunks_by_merging_requirements_from_paths(self.paths, previously_merged=[])
                        except RequirementNotSatisfiedException, rnse:
                            print "A requirement could not be satisfied for %s\n\n%s\n" % (resource.path_to_file, rnse)
                            return -1

                        for chunk in chunks:
                            analyzers = self.config.get_analyzers_for_resource(chunk.resource)
                            if analyzers:
                                for analyzer in analyzers:
                                    print 'Analysis:%s:%s' % (analyzer.__class__, chunk.resource.path_to_file)
                                    analysis = analyzer.analyze(chunk.resource)
                                    print analysis
                                    if not analysis.good:
                                        return -1

                        merged_content = ''.join([chunk.content for chunk in chunks])

                        output_file_name = os.path.join(self.output_dir, file_name)
                        f = open(output_file_name, 'w')
                        try:
                            f.write(merged_content)
                        finally:
                            f.flush()
                            f.close()

                        print "Created %s" % output_file_name

                        # TODO: Process chunks to prevent reminification
                        output_resource = Resource(output_file_name)
                        minifier = self.config.get_minifier_for_file_type(output_resource.file_type)
                        if minifier and not output_resource.minified:
                            minification = minifier.minify(output_resource)
                            if not minification.good:
                                print minification
                                return -1
                            minified_output_file_path = os.path.join(self.output_dir, output_resource.minified_file_name)
                            f = open(minified_output_file_path, 'w')
                            try:
                                f.write(minification.content)
                            finally:
                                f.flush()
                                f.close()

        except Exception:
            traceback.print_exc(file=sys.stderr)
            return -1

        return 0

    @staticmethod
    def main():
        parser = optparse.OptionParser("""usage %prog [options] [file1 [file2 [fileN]]]

If no file arguments are specified, blend searches the specified
paths and processes any and all files that require other files.

If no paths are specified, the current working directory is
searched for required files.

If no output path is specified, an output directory is created in the
current working directory and all outputs are written to that directory.""")

        parser.add_option("-o", "--output",
            default=Application.DEFAULT_OUTPUT_DIR,
            dest='output_dir',
            metavar='OUTPUT',
            help="where the file output will be written")

        parser.add_option("-p", "--path",
            default=Application.DEFAULT_PATH_LIST,
            dest='path',
            metavar='PATH',
            action='append',
            help='a directory to be searched for required files (multiple directories can specified by repeating the flag)')

        parser.add_option("-s", "--skipcwd",
            default=not Application.DEFAULT_INCLUDE_CWD,
            dest='skip_cwd',
            metavar='ENV',
            action='store_true',
            help='exclude the current working directory from the search path')

        parser.add_option("-c", "--config",
            default=Application.DEFAULT_CONFIG_FILE_PATH,
            dest='config_file_path',
            metavar='CONFIG',
            help='the JSON format config file from which to load application settings')

        options, arguments = parser.parse_args()

        file_list = arguments or []

        app = Application(options.path, not options.skip_cwd, file_list, options.output_dir, options.config_file_path)
        sys.exit(app.run())

if __name__ == '__main__':
    Application.main()
