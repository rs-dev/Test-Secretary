from dateutil import tz
from datetime import datetime

from django.db import models
from django.core import urlresolvers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django_extensions.db.fields import ModificationDateTimeField
from django.utils.translation import ugettext as _


STATUS = (('NT', 'untested'),
          ('OK', 'success'),
          ('NOK', 'failed'),
          ('DN', 'decision needed'))


class AdminUrlMixIn():
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        name = 'admin:%s_%s_change' % (content_type.app_label,
                                       content_type.model)
        return urlresolvers.reverse(name, args=(self.pk,))


class Application(models.Model, AdminUrlMixIn):
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order', 'name')

    @property
    def active_sections(self):
        return self.testsection_set.filter(active=True)


class TestSection(models.Model, AdminUrlMixIn):
    name = models.CharField(max_length=50)
    app = models.ForeignKey(Application)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.app, self.name)

    @property
    def active_testcases(self):
        return self.testcase_set.filter(active=True)

    class Meta:
        unique_together = ('name', 'app')
        ordering = ('app', 'order', 'name')


class TestCase(models.Model, AdminUrlMixIn):
    order = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    section = models.ForeignKey(TestSection)
    active = models.BooleanField(default=True)
    autotest_exists = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    preconditions = models.ManyToManyField('self', through='Precondition',
                                           null=True, blank=True,
                                           symmetrical=False,
                                           related_name='precondition_set')
    action = models.TextField(null=True, blank=True)
    expected = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.section, self.name)

    class Meta:
        get_latest_by = 'pk'
        ordering = ('section', 'order', 'name')


class Precondition(models.Model, AdminUrlMixIn):
    testcase = models.ForeignKey(TestCase, related_name='from_testcase')
    precondition = models.ForeignKey(TestCase, related_name='precondition')
    comment = models.TextField(null=True, blank=True)


class TestRun(models.Model, AdminUrlMixIn):
    name = models.CharField(max_length=50)
    comment = models.TextField(null=True, blank=True)
    version = models.CharField(max_length=40)
    date = models.DateTimeField(default=datetime.now, blank=True)
    testcases = models.ManyToManyField(TestCase, through='TestCaseRun')
    user = models.ForeignKey(User)

    def has_testcase_assigned(self, testcase):
        return TestCaseRun.objects.filter(
            testrun=self, testcase=testcase
        ).exists()

    def __str__(self):
        t = self.date.astimezone(tz.tzlocal())
        timestring = t.strftime('%Y-%m-%d %H:%M')
        return '[%s] %s' % (timestring, self.name)

    @property
    def assigned_applications(self):
        testcase_ids = self.testcaserun_set.values('testcase_id')
        return Application.objects.filter(
            testsection__testcase__id__in=testcase_ids).distinct()

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        permissions = (
            ("view_testruns", _("Can see own tests running")),
            ("view_other_testruns", _("Can see all tests running")),
        )

    @property
    def is_finished(self):
        """ no untested or undecided testcases
        """
        return self.todo_count + self.decision_count == 0

    @property
    def is_success(self):
        """ nothing failed, also check is_finished
            unfinished testruns can also be successfully if nothing failed yet
        """
        return self.failed_count == 0

    @property
    def success_count(self):
        return self.testcaserun_set.filter(status='OK').count()

    @property
    def failed_count(self):
        return self.testcaserun_set.filter(status='NOK').count()

    @property
    def todo_count(self):
        return self.testcaserun_set.filter(status='NT').count()

    @property
    def decision_count(self):
        return self.testcaserun_set.filter(status='DN').count()


class TestCaseRun(models.Model, AdminUrlMixIn):
    testcase = models.ForeignKey(TestCase)
    testrun = models.ForeignKey(TestRun)
    status = models.CharField(max_length=3, choices=STATUS, default='NT')
    comment = models.TextField(null=True, blank=True)
    modified = ModificationDateTimeField(help_text=_('Last Status Change'))
    editor = models.ForeignKey(User, help_text=_('Last Editor'))

    def __str__(self):
        return '%s: %s' % (self.testrun, self.testcase)

    class Meta:
        ordering = ('testcase__section__app__name', 'testcase__section__order',
                    'testcase__section__name', 'testcase__order')
        permissions = (
            ("view_testcaserun_status", _("Can see own tests running")),
        )
