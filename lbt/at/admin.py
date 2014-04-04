#coding:utf-8
from django.contrib import admin
from models import LBTestConfig, DiffResult


class LBTestConfigAdmin(admin.ModelAdmin):
    pass

class DiffResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(LBTestConfig, LBTestConfigAdmin)
admin.site.register(DiffResult, DiffResultAdmin)
