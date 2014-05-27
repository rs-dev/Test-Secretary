from django.db import models


class UnitTest(models.Model):
    test_module = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.name:
            return '%s [%s]' % (self.name, self.test_module)
        else:
            return '%s' % self.test_module

