from django.urls import path, re_path
from user import views


urlpatterns = [
    path('login', views.LoginAPIView.as_view()),
    path('register', views.RegisterCreateAPIView.as_view()),
    # 用户信息
    path('info', views.InfoAPIView.as_view()),
    # 修改密码
    path('setpassword', views.SetPWDAPIView.as_view()),
    # 校验手机号是否注册接口
    path('check', views.CheckPhoneAPIView.as_view()),
    # 发送验证码接口
    path('sms', views.SMSAPIView.as_view()),

    # 用户收藏
    path('fav', views.FavMovieAPIView.as_view()),
    # 用户点赞
    path('up', views.UpMovieAPIView.as_view()),
    # 用户评论电影
    path('comment', views.CommentAPIView.as_view()),
    # 用户评论电影台词
    path('linescomment', views.LinesCommentAPIView.as_view()),
    # 用户点赞收藏标识接口
    path('upandfav', views.IsUpAndIsFavAPIView.as_view()),
    # 用户收藏
    path('favorite', views.FavoriteAPIView.as_view()),
    # 发送邮件重置密码
    path('reset', views.ResetPasswordAPIVIew.as_view()),

]
