
from django_filters.rest_framework import FilterSet

from movie import models


# 标签筛选类
class TagFilterSet(FilterSet):
    """标签筛选类"""
    class Meta:
        model = models.Movie
        fields = ['name']