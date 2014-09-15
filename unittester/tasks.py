import sys
import unittest
import logging
import importlib
import json

from celery import shared_task

from test_secretary import settings
from .config import TESTDIRECTORIES
from .models import *
from test_secretary.models import *


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
    test_result = unittest.TextTestRunner().run(suite)
    return test_result


@shared_task
def run_testcaserun(tcrid):
    testcaserun = TestCaseRun.objects.get(pk=tcrid)
    test_results = []
    descriptions = []
    test_runs = []
    unittests = testcaserun.testcase.unittest_set.all()

    for test in unittests:
        test_result = run_test(test.test_module)
        utr = UnitTestRun(unittest=test, testcaserun=testcaserun)
        errors, failures = test_result.errors, test_result.failures
        utr.errors = len(errors)
        utr.failures = len(failures)
        utr.tests_run = test_result.testsRun
        description = '\n'.join(map(lambda x: x[1], errors+failures))
        utr.description = description
        descriptions.append(description)
        utr.save()
        test_results.append(test_result)
        test_runs.append(utr)

    is_success = all([run.wasSuccessful() for run in test_results])
    if testcaserun.status == 'NT':
        testcaserun.status = 'OK' if is_success else 'NOK'
        if not testcaserun.comment:
            testcaserun.comment = ('\n'+'='*79+'\n').join(descriptions)
        testcaserun.save()

    return testcaserun.status
