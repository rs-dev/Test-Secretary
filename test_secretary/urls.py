from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import unittester.urls

urlpatterns = patterns('',
    url(r'^$', 'test_secretary.views.home', name='overview'),
    url(r'^testrun/(?P<rid>\d+)/?$', 'test_secretary.views.testrun_overview', name='testrun_overview'),
    url(r'^testrun/new/?$', 'test_secretary.views.new_testrun', name='new_testrun'),
    url(r'^testcaserun/edit/(?P<trid>\d+)/(?P<elemno>\d+)/?$', 'test_secretary.views.edit_testcaserun', name='edit_testcaserun_multiple'),
    url(r'^testcaserun/edit/(?P<tcrid>\d+)/?$', 'test_secretary.views.edit_testcaserun_single', name='edit_testcaserun_single'),
    url(r'^testcaserun/setstatus/(?P<tcrid>\d+)/(?P<status>[A-Z]{2,3})/?$', 'test_secretary.views.set_testcaserun_status', name='set_testcaserun_status'),
    url(r'^app/(?P<aid>\d+)/(?P<all>all)?/?$', 'test_secretary.views.app_overview', name='app_overview'),

    url(r'^unittester/', include(unittester.urls, namespace='unittester')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="generic_login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="generic_logout"),
)
