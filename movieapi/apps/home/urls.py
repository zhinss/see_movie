from django.urls import path, re_path
from home import views

urlpatterns = [
    # 轮播图路由
    path('banner', views.BannerListAPIVIew.as_view()),

]
