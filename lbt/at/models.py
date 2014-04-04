#coding:utf-8
from django.db import models

# Create your models here.
class LBTestConfig(models.Model):
    server_config = models.TextField(verbose_name="服务器配置")
    statistical_result = models.TextField(verbose_name="统计结果", blank=True)
    tested = models.BooleanField(verbose_name="已成功执行")

class DiffResult(models.Model):
    lbt1 = models.ForeignKey(LBTestConfig, verbose_name="测试配置1", related_name="base_lbt")
    lbt2 = models.ForeignKey(LBTestConfig, verbose_name="测试配置2", related_name="next_lbt")
    result = models.FloatField(verbose_name="分配一致的比率")
