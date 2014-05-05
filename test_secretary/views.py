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


def new_testrun(request):
    d = {}
    if request.method == 'POST':
        # TODO
        pass

    d['apps'] = Application.objects.filter(active=True)

    return render(request, 'test_secretary/new_testrun.html', d)
