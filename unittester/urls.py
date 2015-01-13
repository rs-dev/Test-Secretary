from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^testcaserun/run/(?P<tcrid>\d+)/?$',
        'unittester.views.run_testcaserun', name='testcaserun'),
)
