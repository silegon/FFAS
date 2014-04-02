from django.db import models

# Create your models here.
class LBTestConfig(models.Model):
    server_config = models.TextField(verbose_name="服务器配置")
    statistical_result = models.TextField(verbose_name="统计结果")
    success = models.BooleanField(verbose_name="已执行成功")

class DiffResult(models.Models):
    lbt1 = models.ForeignKey(LBTestConfig, verbose_name="测试配置1")
    lbt2 = models.ForeignKey(LBTestConfig, verbose_name="测试配置2")
    result = models.FloatField(verbose_name="分配一致比率")
