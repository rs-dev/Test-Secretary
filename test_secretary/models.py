from datetime import datetime

from django.db import models

STATUS = (('NT', 'untested'),
          ('OK', 'success'),
          ('NOK', 'failed'),
          ('DN', 'decicion needed'))


class Application(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @property
    def active_sections(self):
        return self.testsection_set.filter(active=True)


class TestSection(models.Model):
    name = models.CharField(max_length=50)
    app = models.ForeignKey(Application)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s - %s' % (self.app, self.name)

    @property
    def active_testcases(self):
        return self.testcase_set.filter(active=True)


class TestCase(models.Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    section = models.ForeignKey(TestSection)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    preconditions = models.ManyToManyField('self')
    precondition_comment = models.TextField(null=True, blank=True)
    action = models.TextField(null=True, blank=True)
    expected = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.section, self.name)


class TestRun(models.Model):
    name = models.CharField(max_length=50)
    comment = models.TextField(null=True, blank=True)
    version = models.CharField(max_length=15)
    date = models.DateTimeField(default=datetime.now, blank=True)
    testcases = models.ManyToManyField(TestCase, through='TestCaseRun')

    def __str__(self):
        return '[%s] %s' % (self.date.strftime('%Y-%m-%d %H:%M'), self.name)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']

    @property
    def is_finished(self):
        return self.testcaserun_set.exclude(status='NT').count() == 0

    @property
    def is_success(self):
        return self.testcaserun_set.filter(status='NOK').count() == 0


class TestCaseRun(models.Model):
    testcase = models.ForeignKey(TestCase)
    testrun = models.ForeignKey(TestRun)
    status = models.CharField(max_length=3, choices=STATUS, default='NT')
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.testrun, self.testcase)
