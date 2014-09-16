from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from test_secretary.models import *
from unittester.models import *
from unittester.tasks import run_testcaserun_tests


@login_required
def run_testcaserun(request, tcrid):
    testcaserun = get_object_or_404(TestCaseRun, pk=tcrid)
    unittests = testcaserun.testcase.unittest_set.all()
    d = {'testcaserun': testcaserun,
         'unittests': unittests
        }
    if request.method == 'POST':
        run_testcaserun_tests.delay(tcrid)
        d['queued'] = True

    return render(request, 'unittester/run_testcaserun.html', d)
