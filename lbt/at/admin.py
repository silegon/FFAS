#coding:utf-8
from django.contrib import admin
from models import LBTestConfig

class LBTestConfigAdmin(admin.ModelAdmin):
    list_display = ('server_config', 'statistical_result')


admin.site.register(LBTestConfig, LBTestConfigAdmin)
