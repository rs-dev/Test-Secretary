from django.contrib import admin
from .models import *


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TestSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'app')
    list_filter = ('app',)


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'section', 'active')
    list_filter = ('section', 'active', 'section__app')


class TestCaseRunInline(admin.TabularInline):
    model = TestCaseRun


class TestCaseRunAdmin(admin.ModelAdmin):
    list_display = ('testcase', 'testrun', 'status')
    list_filter = ('testcase', 'testrun', 'status', 'testrun__date')


class TestRunAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'date')
    list_filter = ('version', 'date')

    inlines = [
        TestCaseRunInline,
    ]


admin.site.register(Application, ApplicationAdmin)
admin.site.register(TestSection, TestSectionAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestRun, TestRunAdmin)
admin.site.register(TestCaseRun, TestCaseRunAdmin)
