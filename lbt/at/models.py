#coding:utf-8
from django.db import models

# Create your models here.
class LBTestConfig(models.Model):
    server_config = models.TextField(verbose_name="服务器配置")
    statistical_result = models.TextField(verbose_name="统计结果", blank=True)

    def save(self, *args, **kwargs):
        content = []
        for line in self.server_config.splitlines():
            sline = line.strip()
            content.append(sline)
        self.server_config = "\n".join(content)
        super(LBTestConfig, self).save(*args, **kwargs)
