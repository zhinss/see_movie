import time

from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.models import BaseModel
from movie.models import Movie, Tag, Lines


# 自定义用户表
class MyUser(AbstractUser):
    """自定义用户表"""
    image = models.ImageField(upload_to='user/%Y/%m', verbose_name='用户头像', default='default.jpg', blank=True)
    nick_name = models.CharField(max_length=32, verbose_name='昵称', default=f'用户{time.strftime("%Y%m%d%H%M%S")}'
                                 , blank=True)
    phone = models.CharField(max_length=11, verbose_name='手机号', unique=True)
    is_vip = models.BooleanField(default=False, verbose_name='会员')
    vip_expire_date = models.DateTimeField(null=True, blank=True)
    vip_time = models.CharField(max_length=32, verbose_name='会员到期时间', null=True)
    movie_type = models.ForeignKey(to=Tag, related_name='user_movie_type', verbose_name='感兴趣的类型',
                                   on_delete=models.CASCADE, default=1, db_constraint=False)
    favorites = models.ManyToManyField(to=Movie, through='Favorite', through_fields=('user', 'movie')
                                       , related_name='user_favorite')
    up_movies = models.ManyToManyField(to=Movie, through='UpOrDown', through_fields=('user', 'movie'))

    # 用户感兴趣的分类
    @property
    def fav_type(self):
        return self.movie_type.name

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 用户收藏表
class Favorite(BaseModel):
    """用户收藏表"""
    user = models.ForeignKey(to=MyUser, verbose_name='用户ID', on_delete=models.CASCADE, db_constraint=False)
    movie = models.ForeignKey(to=Movie, verbose_name='电影ID', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        verbose_name = '收藏表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'用户{self.user.username}收藏了电影{self.movie.name}'


# 点赞点踩表
class UpOrDown(BaseModel):
    """点赞点踩表"""
    user = models.ForeignKey(to=MyUser, verbose_name='用户ID', on_delete=models.CASCADE, db_constraint=False)
    movie = models.ForeignKey(to=Movie, verbose_name='电影ID', on_delete=models.CASCADE, db_constraint=False)
    is_up = models.BooleanField(verbose_name='是否点赞')

    class Meta:
        verbose_name = '点赞表'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.is_up:
            return f'用户{self.user.username}点赞了电影{self.movie.name}'
        return f'用户{self.user.username}点踩了电影{self.movie.name}'


# 评论表
class Comment(BaseModel):
    """评论表"""
    user = models.ForeignKey(to=MyUser, verbose_name='用户', on_delete=models.CASCADE, db_constraint=False)
    movie = models.ForeignKey(to=Movie, verbose_name='电影', on_delete=models.CASCADE, db_constraint=False)
    content = models.CharField(max_length=256, verbose_name='评论内容')
    parent = models.ForeignKey(to='self', verbose_name='父评论', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = '电影评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'用户{self.user.username}评论了电影{self.movie.name}'


# 电影台词评论表
class LinesComment(BaseModel):
    """电影台词评论表"""

    user = models.ForeignKey(to=MyUser, verbose_name='用户', on_delete=models.CASCADE, db_constraint=False)
    lines = models.ForeignKey(to=Lines, verbose_name='台词', on_delete=models.CASCADE, db_constraint=False)
    content = models.CharField(max_length=256, verbose_name='评论内容')
    parent = models.ForeignKey(to='self', verbose_name='父评论', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = '台词评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'用户{self.user.username}评论了电影{self.lines.movie_name}的台词'