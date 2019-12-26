from rest_framework import serializers

from movie import models


# 标签序列化类
class TagModelSerializer(serializers.ModelSerializer):
    """标签序列化类"""
    class Meta:
        model = models.Tag
        fields = ['pk', 'name', 'type', 'status']


# 电影序列化类
class MovieModelSerializer(serializers.ModelSerializer):
    """电影序列化类"""
    class Meta:
        model = models.Movie
        fields = ['pk', 'name', 'desc', 'image', 'url', 'is_vip', 'up_num', 'movie_type', 'fav_num', 'release_time']


# 电影详情序列化类
class MovieDetailSerializerModel(serializers.ModelSerializer):
    """电影详情序列化类"""
    class Meta:
        model = models.Movie
        fields = [
            'name',
            'desc',
            'image',
            'url',
            'is_vip',
            'up_num',
            'com_num',
            'fav_num',
            'release_time',
            'movie_comment',
        ]


# 搜索电影序列化类
class SearchSerializerModel(serializers.ModelSerializer):
    """搜索电影序列化类"""
    class Meta:
        model = models.Movie
        fields = ['pk', 'name', 'desc', 'image', 'url', 'is_vip', 'up_num', 'movie_type']


# 推荐电影序列化类
class RecommendModelSerializer(serializers.ModelSerializer):
    """推荐电影序列化类"""
    class Meta:
        model = models.Movie
        fields = ['pk', 'name', 'image', 'url', 'is_vip', 'fav_num', 'movie_type']


# 电影台词序列化类
class LinesModelSerializer(serializers.ModelSerializer):
    """电影台词序列化类"""
    class Meta:
        model = models.Lines
        fields = ['pk', 'movie_name', 'content', 'lines_comment']
