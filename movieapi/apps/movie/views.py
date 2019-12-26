import random

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from movie import models
from movie import serializers
from movie.filters import TagFilterSet


# 标签接口
class TagListAPIView(ListAPIView):
    """标签接口"""
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagModelSerializer


# # 电影接口
# class MovieListAPIView(ListAPIView):
#     """电影接口"""
#     queryset = models.Movie.objects.filter(is_delete=False).order_by('-up_num').all()
#     serializer_class = serializers.MovieModelSerializer
#
#     filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
#
#     # 参与筛选的字段
#     filter_fields = ['type']
#
#     # 参与筛选的类
#     filter_class = TagFilterSet


# 电影接口
class MovieListAPIView(APIView):
    """电影接口"""
    def get(self, request, *args, **kwargs):
        movie_type = request.query_params.get('tag')
        if movie_type == 'VIP':
            movies = models.Movie.objects.filter(is_vip=True, is_delete=False).order_by('-up_num').all()
        elif not movie_type:
            movies = models.Movie.objects.filter(is_delete=False).order_by('-up_num').all()
        else:
            tag2movies = models.Tag.objects.filter(name=movie_type).first().tag2movie_set.all()[0:4]
            movies = []
            for tag2movie in tag2movies:
                movies.append(tag2movie.movie)

        movie_ser = serializers.MovieModelSerializer(movies, many=True, context={'request': request}).data

        return Response(data=movie_ser)


# 电影详情接口
class MovieDetailAPIView(APIView):
    """电影详情接口"""
    def get(self, request, *args, **kwargs):
        movie_id = request.query_params.get('id')

        print(request.query_params)

        movie_obj = models.Movie.objects.filter(pk=movie_id).first()

        movie_ser = serializers.MovieDetailSerializerModel(movie_obj, context={'request': request}).data

        return Response(data=movie_ser)


# 电影搜索接口
class SearchAPIView(ListAPIView):
    """电影搜索接口"""
    queryset = models.Movie.objects.filter(is_delete=False).order_by('-fav_num').all()
    serializer_class = serializers.SearchSerializerModel

    # 配置过滤器类
    filter_backends = [SearchFilter]
    # 配置参与搜索的字段
    search_fields = ['name']


# 推荐电影接口
class RecommendListAPIView(ListAPIView):
    """推荐电影接口"""
    queryset = models.Movie.objects.filter(is_delete=False).order_by('-fav_num').all()[:4]
    serializer_class = serializers.RecommendModelSerializer


# 电影台词接口
class LinesListAPIView(ListAPIView):
    """电影台词接口"""
    queryset = models.Lines.objects.all().order_by('-order')
    serializer_class = serializers.LinesModelSerializer


# 电影台词详情接口
class LinesDetailAPIView(APIView):
    """电影台词详情接口"""
    def get(self, request, *args, **kwargs):
        lines_id = request.query_params.get('lines_id')

        lines_obj = models.Lines.objects.filter(pk=lines_id).first()

        lines_ser = serializers.LinesModelSerializer(lines_obj).data

        return Response(data=lines_ser)
