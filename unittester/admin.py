from django.contrib import admin
from .models import *

class UnitTestAdmin(admin.ModelAdmin):
    list_display = ('test_module', 'name')
    search_fields = ('test_module', 'name')
    exclude = ('testcases', )


class UnitTestRunAdmin(admin.ModelAdmin):
    list_display = ('unittest', 'testcaserun', 'date', 'tests_run', 'errors', 'failures')
    list_filter = ('unittest', 'testcaserun', 'date')

admin.site.register(UnitTest, UnitTestAdmin)
admin.site.register(UnitTestRun, UnitTestRunAdmin)
