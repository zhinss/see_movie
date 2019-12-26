from django.db import models


# 基类
class BaseModel(models.Model):
    """基类"""
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
