from django.urls import path, re_path

from order import views

urlpatterns = [
    # 支付接口
    path('pay', views.PayAPIView.as_view()),
    # 支付成功回调接口
    path('success', views.PaySuccessAPIView.as_view()),
]
