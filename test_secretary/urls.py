from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'test_secretary.views.home', name='home'),
    url(r'^testrun/(?P<rid>\d+)/?$', 'test_secretary.views.testrun_overview', name='testrun_overview'),
    url(r'^testrun/new/?$', 'test_secretary.views.new_testrun', name='new_testrun'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
