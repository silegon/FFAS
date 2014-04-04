#coding:utf-8
from django.contrib import admin
from models import LBTestConfig, DiffResult


class LBTestConfigAdmin(admin.ModelAdmin):
    list_display = ('server_config', 'statistical_result')

class DiffResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(LBTestConfig, LBTestConfigAdmin)
admin.site.register(DiffResult, DiffResultAdmin)
