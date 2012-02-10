#!/usr/bin/env python

import unittest, logging
from optparse import OptionParser

import os
import sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    # TODO: Make this dynamic

    from pipeline.test.TestApplication import TestApplication
    from pipeline.test.TestEnvironment import TestEnvironment
    from pipeline.test.TestPipeline import TestPipeline
    from pipeline.test.TestRequirement import TestRequirement
    from pipeline.test.TestResource import TestResource

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEnvironment))
    suite.addTest(unittest.makeSuite(TestApplication))
    suite.addTest(unittest.makeSuite(TestPipeline))
    suite.addTest(unittest.makeSuite(TestRequirement))
    suite.addTest(unittest.makeSuite(TestResource))

    unittest.TextTestRunner(verbosity=2).run(suite)
