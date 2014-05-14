import re
from datetime import datetime, date

from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import *
from .forms import TestCaseRunForm


def home(request):
    d = {}
    d['apps'] = Application.objects.all()
    d['testruns'] = TestRun.objects.all()
    return render(request, 'test_secretary/overview.html', d)


def app_overview(request, aid):
    d = {}
    app = Application.objects.get(pk=aid)
    d['app'] = app
    return render(request, 'test_secretary/app_overview.html', d)


def testrun_overview(request, rid):
    d = {}
    testrun = TestRun.objects.get(pk=rid)
    d['testrun'] = testrun
    d['testcaseruns'] = testrun.testcaserun_set.all()

    return render(request, 'test_secretary/testrun_overview.html', d)


TCREGEX = re.compile('testcase(?P<tcid>\d+)')

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
            testrun = TestRun(name=name, comment=comment, version=version)
            testrun.save()
            for testcase in testcases:
                tcr = TestCaseRun(testcase=testcase, testrun=testrun)
                tcr.save()
            return HttpResponseRedirect(reverse('testrun_overview', kwargs={'rid': testrun.pk}))
        else:
            d['errmsg'] = 'No testcases selected'

    d['apps'] = Application.objects.filter(active=True)

    return render(request, 'test_secretary/new_testrun.html', d)

def edit_testcaserun(request, tcrid):
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
    return render(request, 'test_secretary/edit_testcaserun.html', d)
