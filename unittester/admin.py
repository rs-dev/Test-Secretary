from django.contrib import admin
from .models import *

class UnitTestAdmin(admin.ModelAdmin):
    list_display = ('test_module', 'name')
    search_fields = ('test_module', 'name')

admin.site.register(UnitTest, UnitTestAdmin)
