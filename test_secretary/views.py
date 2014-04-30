from django.shortcuts import render

from .models import *

def home(request):
    d = {}
    d['apps'] = Application.objects.all()
    d['testruns'] = TestRun.objects.all()
    return render(request, 'test_secretary/overview.html', d)
