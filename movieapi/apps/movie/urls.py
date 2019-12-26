from django.urls import path, re_path

from movie import views

urlpatterns = [
    # 电影标签
    path('tag', views.TagListAPIView.as_view()),
    # 电影列表
    path('movie', views.MovieListAPIView.as_view()),
    # 电影详情
    path('detail', views.MovieDetailAPIView.as_view()),
    # 电影搜索
    path('search', views.SearchAPIView.as_view()),
    # 电影推荐
    path('recommend', views.RecommendListAPIView.as_view()),
    # 电影台词
    path('lines', views.LinesListAPIView.as_view()),
    # 电影台词详情
    path('lines_detail', views.LinesDetailAPIView.as_view()),
]
