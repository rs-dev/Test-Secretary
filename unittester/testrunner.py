import sys
import unittest
import logging
import importlib

from .config import TESTDIRECTORIES


def run_test(testcase):
    sys.path += TESTDIRECTORIES
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
    return unittest.TextTestRunner().run(suite)


def run_tests(testcases):
    test_results = []

    if isinstance(testcases, str) or isinstance(testcases, unittest.TestCase):
        testcases = [testcases]

    for testcase in testcases:
        test_results.append(run_test(testcase))

    return test_results
