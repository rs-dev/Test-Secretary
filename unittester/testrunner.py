import sys
import unittest
import logging
import importlib

from .config import TESTDIRECTORIES


def run_tests(testcases):
    sys.path += TESTDIRECTORIES
    test_results = []

    if isinstance(testcases, str) or isinstance(testcase, unittest.TestCase):
        testcases = [testcases]

    for testcase in testcases:
        if isinstance(testcase, str):
            mod, _, klass = testcase.rpartition('.')
            try:
                mod = __import__(mod, fromlist=[klass])
                testcase = getattr(mod, klass)
            except (AttributeError, ImportError):
                logging.error('No such module:', testcase)
                return None
        elif not isinstance(testcase, unittest.TestCase):
            logging.error('Given test case neither String nor unittest.TestCase:', testcase)
            return None

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(testcase)
        test_results.append(unittest.TextTestRunner().run(suite))
    return test_results
