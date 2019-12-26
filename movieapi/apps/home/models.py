from django.db import models
from utils.models import BaseModel


# 轮播图
class Banner(BaseModel):
    """轮播图"""
    name = models.CharField(max_length=11, verbose_name='名字')
    image = models.ImageField(upload_to='home/%Y/%m', verbose_name='轮播图')
    is_show = models.BooleanField(verbose_name='是否上线')
    order = models.IntegerField(verbose_name='显示顺序')
    movie_id = models.IntegerField(verbose_name='电影ID')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


