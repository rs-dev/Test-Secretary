import re
from datetime import datetime, date

from django.shortcuts import render

from .models import *


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
        # extract ids from post elements
        for elem in request.POST.keys():
            print(elem)
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
        else:
            d['errmsg'] = 'No testcases selected'

    d['apps'] = Application.objects.filter(active=True)

    return render(request, 'test_secretary/new_testrun.html', d)
