from datetime import datetime

from django.db import models

STATUS = (('NT', 'untested'),
          ('OK', 'success'),
          ('NOK', 'failed'),
          ('DN', 'decicion needed'))


class Application(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TestSection(models.Model):
    name = models.CharField(max_length=50)
    app = models.ForeignKey(Application)

    def __str__(self):
        return '%s - %s' % (self.app, self.name)


class TestCase(models.Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    section = models.ForeignKey(TestSection)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    precondition = models.TextField(null=True, blank=True)
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


class TestCaseRun(models.Model):
    testcase = models.ForeignKey(TestCase)
    testrun = models.ForeignKey(TestRun)
    status = models.CharField(max_length=3, choices=STATUS, default='NT')
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.testrun, self.testcase)
