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
import re
import platform
import subprocess
from Analyzer import Analyzer
from helpers import first_file_name_in_path_matching_regex


class JsLintComplaint(object):
    def __init__(self, complaint):
        lines = complaint.split('\n')
        regex_match = re.search("line ([0-9]*) character ([0-9]*):(.*)", lines[0])
        if regex_match:
            self.complaint = regex_match.group(2).strip()
            for line in lines:
                self.complaint += "\n" + line
            if len(self.complaint.strip()):
                try:
                    self.line_number = int(regex_match.group(0))
                except:
                    self.line_number = -1
                try:
                    self.column_number = int(regex_match.group(1))
                except:
                    self.column_number = -1
            else:
                self.line_number = -1
                self.column_number = -1
                self.complaint = complaint
        else:
            self.line_number = -1
            self.column_number = -1
            self.complaint = complaint

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        if self.line_number > 0:
            if self.column_number > 0:
                return 'Line %d:%d - %s' % (self.line_number, self.column_number, self.complaint)
            else:
                return 'Line %d - %s' % (self.line_number, self.complaint)
        else:
            return self.complaint


class JSLintAnalyzer(Analyzer):

    def __init__(self, lib_path=None, use_nodejs_if_available=True):
        self._js_lint_proc_args = None
        self._module_path = os.path.dirname(os.path.realpath(__file__))
        self._lib_path = lib_path or os.path.join(self._module_path, 'lib')
        self._jslint_script_regex = re.compile(r'^jslint.*\.js$')
        self._js_lint_script_file_path = first_file_name_in_path_matching_regex(self._lib_path, self._jslint_script_regex)
        self._rhino_jar_regex = re.compile(r'^js\.jar$')
        self._rhino_jar_file_path = first_file_name_in_path_matching_regex(self._lib_path, self._rhino_jar_regex)
        self._lib_message_list = []

        if self._js_lint_proc_args is None and platform.system() == 'Windows':
            # Windows Script Host has two versions, wscript.exe which pops up
            # a window and cscript.exe which does not.
            self._js_lint_proc_args = ["cscript.exe", "//I", "//Nologo", self._js_lint_script_file_path]
            self._lib_message_list.append("Using cscript.exe to run JSLint")

        if self._js_lint_proc_args is None and use_nodejs_if_available:
            null_file = open(os.devnull, 'w')
            try:
                subprocess.check_call(['node', '--help'], stdout=null_file, stderr=null_file)
                self._js_lint_proc_args = ["node", self._js_lint_script_file_path]
                self._lib_message_list.append("Using node.js to run JSLint")
            except Exception:
                self._lib_message_list.append("Cannot use node.js to run JSLint because it was not found on the PATH")
            finally:
                null_file.close()

        if self._js_lint_proc_args is None:
            if self._rhino_jar_file_path:
                self._js_lint_proc_args = ["java", "-jar", self._rhino_jar_file_path, self._js_lint_script_file_path]
                self._lib_message_list.append("Using Rhino to run JSLint")
            else:
                self._lib_message_list.append("Cannot use Rhino to run JSLint because js.jar could not be found in in %r" % self._lib_path)

    def analyze(self, resource):
        analysis = Analyzer.analyze(self, resource)
        analysis.add_messages(self._lib_message_list)
        if self._js_lint_proc_args is None:
            analysis.mark_as_bad()
            analysis.add_error('No suitable JSLint runner (cscript.exe, node.js or rhino) could be found.')
            return analysis

        try:
            js_lint_proc = subprocess.Popen(self._js_lint_proc_args, -1, None, subprocess.PIPE,
                subprocess.PIPE, subprocess.PIPE)
            js_lint_proc_outputs = js_lint_proc.communicate(resource.content)
        except Exception as e:
            analysis.add_error("An exception what thrown while running JsLint: " + str(e))
            return analysis

        # The JSLint process returns 1 if it finds lint
        if js_lint_proc.returncode != 0 and js_lint_proc.returncode != 1:
            analysis.add_error('The JSLint process exited with return code %d\nArguments: %s\n Output: %s'
                % (js_lint_proc.returncode, self._js_lint_proc_args, js_lint_proc_outputs))
            return analysis

        analysis.mark_as_good()  # Assume that JSLint produced no complaints until parsing one from the process output

        for js_lint_proc_output in js_lint_proc_outputs:
            js_lint_complaints = js_lint_proc_output.split("Lint at ")
            for complaint in js_lint_complaints:
                if len(complaint.strip()):
                    analysis.mark_as_bad()
                    js_lint_complaint = JsLintComplaint(complaint)
                    analysis.add_error(str(js_lint_complaint))

        return analysis
