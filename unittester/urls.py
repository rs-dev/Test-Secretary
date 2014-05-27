from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^testcaserun/run/(?P<tcrid>\d+)/?$', 'unittester.views.run_testcaserun_single', name='run_testcaserun_single'),
)
