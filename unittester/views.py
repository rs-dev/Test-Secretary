from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from test_secretary.models import *
from unittester.models import *
from unittester.testrunner import run_test


def run_testcaserun_single(request, tcrid):
    testcaserun = get_object_or_404(TestCaseRun, pk=tcrid)
    unittests = testcaserun.testcase.unittest_set.all()
    d = {'testcaserun': testcaserun,
         'unittests': unittests
        }
    if request.method == 'POST':
        test_results = []
        test_runs = []

        for test in unittests:
            test_result = run_test(test.test_module)
            utr = UnitTestRun(unittest=test, testcaserun=testcaserun)
            errors, failures = test_result.errors, test_result.failures
            utr.errors = len(errors)
            utr.failures = len(failures)
            utr.tests_run = test_result.testsRun
            description = '\n'.join(map(lambda x: x[1], errors+failures))
            utr.description = description
            utr.save()
            test_runs.append(utr)

        d['test_results'] = test_results
        d['test_runs'] = test_runs

    return render(request, 'unittester/run_testcaserun_single.html', d)
