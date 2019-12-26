from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.conf import settings
from django.core.cache import cache

from home import models
from home.serializers import BannerModelSerializer


# 轮播图接口
class BannerListAPIVIew(ListAPIView):
    """轮播图接口"""
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('-order')[:settings.BANNER_NUM]
    serializer_class = BannerModelSerializer

    # 自定义get方法实现轮播图缓存
    def get(self, request, *args, **kwargs):

        banner_list = cache.get('banner_list')
        # banner_list = 0

        if not banner_list:

            response = self.list(request, *args, **kwargs)
            # response.data不是json数据，是drf中自定义的ReturnList类
            # 缓存不设置过期时间，交给celery定期更新
            cache.set('banner_list', response.data)
            return response

        return Response(banner_list)
