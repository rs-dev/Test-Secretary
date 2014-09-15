from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from test_secretary.models import *
from unittester.models import *
from unittester.tasks import run_testcaserun


def run_testcaserun_single(request, tcrid):
    testcaserun = get_object_or_404(TestCaseRun, pk=tcrid)
    unittests = testcaserun.testcase.unittest_set.all()
    d = {'testcaserun': testcaserun,
         'unittests': unittests
        }
    if request.method == 'POST':
        run_testcaserun(tcrid)

    return render(request, 'unittester/run_testcaserun_single.html', d)
