#!/usr/bin/env python

import unittest, logging
from optparse import OptionParser

import os
import sys
import inspect
import pkgutil

if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    from pipeline import test

    suite = unittest.TestSuite()

    for importer, modname, ispkg in pkgutil.iter_modules(test.__path__):
        module = __import__('pipeline.test.' + modname, globals(), locals(), [modname])
        for name, class_obj in inspect.getmembers(module):
            if inspect.isclass(class_obj):
                suite.addTest(unittest.makeSuite(class_obj))

    unittest.TextTestRunner(verbosity=2).run(suite)
