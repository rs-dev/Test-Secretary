import re
import itertools
from datetime import datetime, date

from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import TestCaseRunForm
from unittester.testrunner import run_tests


def home(request):
    d = {}
    d['apps'] = Application.objects.all()
    testruns = {'own': [], 'other': []}
    testruns['own'] = TestRun.objects.filter(user=request.user)
    testruns['other'] = TestRun.objects.exclude(user=request.user)

    d['testruns'] = testruns
    return render(request, 'test_secretary/overview.html', d)


def app_overview(request, aid):
    d = {}
    app = Application.objects.get(pk=aid)
    d['app'] = app
    return render(request, 'test_secretary/app_overview.html', d)


def testrun_overview(request, rid):
    d = {'counter': itertools.count()}
    testrun = TestRun.objects.get(pk=rid)
    d['testrun'] = testrun
    d['testcaseruns'] = testrun.testcaserun_set.all()

    return render(request, 'test_secretary/testrun_overview.html', d)


TCREGEX = re.compile('testcase(?P<tcid>\d+)')

@login_required
def new_testrun(request):
    d = {}
    if request.method == 'POST':
        name = request.POST.get('name', 'TestRun %s'% datetime.now().strftime('%c'))
        comment = request.POST.get('comment', None)
        version = request.POST.get('version', 'undefined')
        testcase_ids = [TCREGEX.match(elem).groupdict()['tcid'] for elem in request.POST if TCREGEX.match(elem)]
        # get TestCases from ids
        testcases = [TestCase.objects.get(pk=tcid) for tcid in testcase_ids]

        if testcases:
            print('Saving new TestRun: %s' % name)
            testrun = TestRun(name=name, comment=comment, version=version,
                              user=request.user)
            testrun.save()
            for testcase in testcases:
                tcr = TestCaseRun(testcase=testcase, testrun=testrun)
                tcr.save()
            return HttpResponseRedirect(reverse('testrun_overview', kwargs={'rid': testrun.pk}))
        else:
            d['errmsg'] = 'No testcases selected'

    d['apps'] = Application.objects.filter(active=True)

    return render(request, 'test_secretary/new_testrun.html', d)


def edit_testcaserun_single(request, tcrid):
    d = {'saved': False}

    testcaserun = get_object_or_404(TestCaseRun, pk=tcrid)
    d['testcaserun'] = testcaserun

    if request.method == 'POST':
        testcaserun_form = TestCaseRunForm(request.POST, instance=testcaserun)
        if testcaserun_form.is_valid():
            testcaserun_form.save()
            d['saved'] = True
    else:
        testcaserun_form = TestCaseRunForm(instance=testcaserun)

    d['testcaserun_form'] = testcaserun_form
    return render(request, 'test_secretary/edit_testcaserun_single.html', d)


def edit_testcaserun(request, trid, elemno):
    d = {'saved': False}
    elemno = int(elemno)
    d['elemno'] = elemno

    testrun = get_object_or_404(TestRun, pk=trid)
    testcaseruns = TestCaseRun.objects.filter(testrun=testrun)

    tcr_count = testcaseruns.count()
    if elemno < tcr_count:
        testcaserun = testcaseruns[elemno]
    else:
        testcaserun = testcaseruns[tcr_count-1]
        d['elemno'] = tcr_count-1
    d['testcaserun'] = testcaserun

    is_last = elemno >= tcr_count-1
    d['is_last'] = is_last

    if request.method == 'POST':
        testcaserun_form = TestCaseRunForm(request.POST, instance=testcaserun)
        if testcaserun_form.is_valid():
            testcaserun_form.save()
            d['saved'] = True
    else:
        testcaserun_form = TestCaseRunForm(instance=testcaserun)

    d['testcaserun_form'] = testcaserun_form
    return render(request, 'test_secretary/edit_testcaserun_multiple.html', d)


def set_testcaserun_status(request, tcrid, status):
    testcaserun = get_object_or_404(TestCaseRun, pk=tcrid)
    if status in list(zip(*STATUS))[0]:
        testcaserun.status = status
        testcaserun.save()
    return HttpResponse('')
