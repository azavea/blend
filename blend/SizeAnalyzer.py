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

from Analyzer import Analyzer
from Analysis import Analysis

class SizeAnalyzer(Analyzer):

    def analyze(self, resource):
        analysis = Analyzer.analyze(self, resource)
        # This analyzer only computes the size of the content, it does not judge the quality
        lines = resource.content.split('\n')
        analysis.good = True
        if (len(lines) == 1):
            line_noun = 'line'
        else:
            line_noun = 'lines'
        char_count = reduce(lambda count, x: count+len(x), lines, 0)
        if (analysis.messages is None):
            analysis.messages = []
        analysis.messages.append('%d characters in %d %s' % (char_count, len(lines), line_noun))

        return analysis