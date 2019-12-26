
from django.db import models
from utils.models import BaseModel


# 电影表
class Movie(BaseModel):
    """电影表"""
    name = models.CharField(max_length=16, verbose_name='电影名')
    desc = models.TextField(verbose_name='简介')
    image = models.ImageField(upload_to='movie/%Y/%m', verbose_name='电影图', blank=True)
    url = models.URLField(verbose_name='电影链接')
    is_vip = models.BooleanField(verbose_name='是否为VIP电影')
    up_num = models.IntegerField(verbose_name='点赞数')
    down_num = models.IntegerField(verbose_name='点踩数')
    com_num = models.IntegerField(verbose_name='评论数')
    fav_num = models.IntegerField(verbose_name='收藏数')
    release_time = models.DateTimeField(verbose_name='上映时间')

    # 电影评论
    @property
    def movie_comment(self):
        comment_list = self.comment_set.all()
        movies_comment = []
        for comment in comment_list:
            movies_comment.append({
                'user': comment.user.username,
                'content': comment.content,
                'created_time': comment.created_time
            })
        return movies_comment

    # 电影类型
    @property
    def movie_type(self):
        tag_list = self.tag2movie_set.all()
        type_list = []
        for tag in tag_list:
            type_list.append(tag.tag.name)
        return type_list

    class Meta:
        verbose_name = '电影表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 标签表
class Tag(BaseModel):
    """标签表"""
    name = models.CharField(max_length=11, verbose_name='标签名')
    movie = models.ManyToManyField(to=Movie, through='Tag2Movie', through_fields=('tag', 'movie'))

    @property
    def type(self):
        return self.name

    @property
    def status(self):
        return False

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 电影标签表
class Tag2Movie(BaseModel):
    """电影标签表"""
    tag = models.ForeignKey(to=Tag, verbose_name='标签', on_delete=models.CASCADE, db_constraint=False)
    movie = models.ForeignKey(to=Movie, verbose_name='电影', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        verbose_name = '电影标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'电影{self.movie.name}的标签是{self.tag.name}'


# 演员表
class Performer(BaseModel):
    """演员表"""
    choices = ((0, '男'), (1, '女'))

    name = models.CharField(max_length=11, verbose_name='名字')
    gender = models.IntegerField(choices=choices, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    star_time = models.DateTimeField()

    class Meta:
        verbose_name = '演员表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 电影演员表
class Per2Movie(BaseModel):
    """电影演员表"""
    performer = models.ForeignKey(to=Performer, verbose_name='演员', on_delete=models.CASCADE, db_constraint=False)
    movie = models.ForeignKey(to=Movie, verbose_name='电影', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        verbose_name = '电影演员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'演员{self.performer.name}出演了电影{self.movie}'


# 电影台词表
class Lines(BaseModel):
    """电影台词表"""
    movie_name = models.CharField(max_length=32, verbose_name='电影', default='这个杀手不太冷')
    content = models.CharField(max_length=256, verbose_name='台词')
    order = models.IntegerField(verbose_name='显示顺序')

    # 电影评论
    @property
    def lines_comment(self):
        comment_list = self.linescomment_set.all()
        lines_comment = []
        for comment in comment_list:
            lines_comment.append({
                'user': comment.user.username,
                'content': comment.content,
                'created_time': comment.created_time
            })
        return lines_comment

    class Meta:
        verbose_name = '电影台词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content



