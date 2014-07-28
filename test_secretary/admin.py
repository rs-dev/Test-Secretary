from django.contrib import admin

from .models import *
from unittester.models import UnitTest


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('order', 'name',)


class TestSectionAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'app')
    list_filter = ('app',)


class UnitTestInline(admin.TabularInline):
    model = UnitTest.testcases.through


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'section', 'active')
    list_filter = ('section', 'active', 'section__app')
    search_fields = ('name', 'description', 'action', 'expected')

    inlines = [
        UnitTestInline,
    ]


class TestCaseRunAdmin(admin.ModelAdmin):
    list_display = ('testcase', 'testrun', 'status', 'editor', 'modified')
    list_filter = ('testcase__section', 'testrun', 'status', 'testrun__date',
                   'editor')


class TestRunAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'date', 'user')
    list_filter = ('version', 'date', 'user')


admin.site.register(Application, ApplicationAdmin)
admin.site.register(TestSection, TestSectionAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestRun, TestRunAdmin)
admin.site.register(TestCaseRun, TestCaseRunAdmin)
