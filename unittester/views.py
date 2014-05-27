from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from test_secretary.models import *
from unittester.testrunner import run_tests


def run_testcaserun_single(request, tcrid):
    testcaserun = get_object_or_404(TestCaseRun, pk=tcrid)
    d['testcaserun'] = testcaserun
    unittests = testcaserun.testrun.unittests.all()
    d['unittests'] = unittests

    if request.method == 'POST':
        d['test_results'] = run_tests(unittests)

    return render(request, 'unittester/run_testcaserun_single.html', d)
