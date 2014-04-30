from django.shortcuts import render

from .models import *

def home(request):
    d = {}
    d['apps'] = Application.objects.all()
    d['testruns'] = TestRun.objects.all()
    return render(request, 'test_secretary/overview.html', d)

def testrun_overview(request, rid):
    d = {}
    testrun = TestRun.objects.get(pk=rid)
    d['testrun'] = testrun
    d['testcaseruns'] = testrun.testcaserun_set.all()

    return render(request, 'test_secretary/testrun_overview.html', d)
