from django.db import models

from test_secretary.models import TestCase, TestCaseRun

class UnitTest(models.Model):
    test_module = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    testcases = models.ManyToManyField(TestCase, null=True, blank=True)

    def __str__(self):
        if self.name:
            return '%s [%s]' % (self.name, self.test_module)
        else:
            return '%s' % self.test_module


class UnitTestRun(models.Model):
    unittest = models.ForeignKey(UnitTest)
    testcaserun = models.ForeignKey(TestCaseRun)
    date = models.DateTimeField(auto_now=True)
    errors = models.PositiveIntegerField(default=0)
    failures = models.PositiveIntegerField(default=0)
    tests_run = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def is_success(self):
        return self.errors+self.failures == 0
