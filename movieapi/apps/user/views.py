import re

from django.conf import settings
from django.core.cache import cache
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from user import serializers
from user import models
from movie.models import Movie, Tag
from utils.response import APIResponse
from libs.tx_sms import send_sms, get_code


# 注册接口
class RegisterCreateAPIView(APIView):
    """注册接口"""

    def post(self, request, *args, **kwargs):
        data = request.data
        user_ser = serializers.RegisterModelSerializer(data=data)

        # 校验
        user_ser.is_valid(raise_exception=True)
        user = user_ser.save()

        return APIResponse(results={
            'username': user.username,
            'phone': user.phone,
            'email': user.email
        })


# 登陆接口
class LoginAPIView(APIView):
    """登陆接口"""
    def post(self, request, *args, **kwargs):
        data = request.data
        user_ser = serializers.LoginModelSerializer(data=data, context={'request': request})
        user_ser.is_valid(raise_exception=True)

        return APIResponse(results={
            'id': user_ser.user.pk,
            'username': user_ser.user.username,
            'is_vip': user_ser.user.is_vip,
            'vip_time': user_ser.user.vip_time,
            'fav_type': user_ser.user.movie_type.name,
            'token': user_ser.token
        })


# 校验手机号接口
class CheckPhoneAPIView(APIView):
    """校验手机号接口"""
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        user = models.MyUser.objects.filter(phone=phone)

        if user:
            return APIResponse(0, '手机号已经注册')
        else:
            return APIResponse(1, '手机未注册')


# 发送短信接口
class SMSAPIView(APIView):
    """发送短信接口"""

    def post(self, request, *args, **kwargs):
        # 获取前端传过来的手机号
        phone = request.data.get('phone')

        if not (phone and re.match(r'^1[3-9][0-9]{9}$', phone)):
            return APIResponse(2, '手机格式有误')
        # if not models.MyUser.objects.filter(phone=phone):
        #     return APIResponse(2, '手机号未注册')

        # 获取验证码
        code = get_code(6)
        # 发送验证码
        result = send_sms(phone, code, settings.CODE_TIME//60)
        if not result:
            return APIResponse(1, '发送验证码失败')

        cache.set(settings.SMS_CACHE_KEY % phone, code, settings.CODE_TIME)

        # 校验发送的验证码与缓存的验证码是否一致
        print('>>>>> %s - %s <<<<<' % (code, cache.get(settings.SMS_CACHE_KEY % phone)))

        return APIResponse(0, '发送验证码成功')


# 获取用户信息接口
class InfoAPIView(APIView):
    """获取用户信息接口"""
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = request.data.get('user_id')

        user = models.MyUser.objects.filter(pk=pk).first()
        user_ser = serializers.InfoModelSerializer(user, context={'request': request}).data

        return APIResponse(results=user_ser)

    def patch(self, request, *args, **kwargs):
        fav_type = request.data.get('fav_type')
        username = request.data.get('username')
        phone = request.data.get('phone')
        email = request.data.get('email')
        image = request.data.get('image')

        fav_obj = Tag.objects.filter(name=fav_type).first()

        user = models.MyUser.objects.filter(username=username).first()

        if image != 'undefined':
            user.image = image

        user.username = username
        user.email = email
        user.movie_type = fav_obj
        user.phone = phone
        user.save()

        return APIResponse(0, '修改成功')


# 修改密码接口
class SetPWDAPIView(APIView):
    """修改密码接口"""
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        new_password = request.data.get('newPassword')
        re_password = request.data.get('repassword')

        if new_password != re_password:
            return APIResponse(1, '两次密码不一致')

        user = models.MyUser.objects.filter(pk=user_id).first()

        if not user.check_password(password):
            return APIResponse(1, '旧密码错误')

        user.set_password(new_password)
        user.save()

        return APIResponse(0, '修改密码成功')


# 用户收藏接口
class FavMovieAPIView(APIView):
    """用户收藏接口"""
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        movie_id = request.query_params.get('movie_id')

        favs = models.Favorite.objects.filter(user_id=user_id, movie_id=movie_id).first()

        if favs:
            return APIResponse(1, '用户已收藏')
        else:
            models.Favorite.objects.create(user_id=user_id, movie_id=movie_id)
            Movie.objects.filter(pk=movie_id).update(fav_num=F('fav_num') + 1)
            return APIResponse(0, '收藏成功')


# 用户点赞接口
class UpMovieAPIView(APIView):
    """用户点赞接口"""
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        movie_id = request.query_params.get('movie_id')

        up_obj = models.UpOrDown.objects.filter(user_id=user_id, movie_id=movie_id).first()

        if up_obj:
            return APIResponse(1, '用户已点过赞')
        else:
            models.UpOrDown.objects.create(user_id=user_id, movie_id=movie_id, is_up=1)
            Movie.objects.filter(pk=movie_id).update(up_num=F('up_num') + 1)
            return APIResponse(0, '点赞成功')


# 用户电影评论接口
class CommentAPIView(APIView):
    """用户评论接口"""
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        movie_id = request.data.get('movie_id')
        content = request.data.get('context')

        models.Comment.objects.create(user_id=user_id, movie_id=movie_id, content=content)
        Movie.objects.filter(pk=movie_id).update(com_num=F('com_num') + 1)

        return APIResponse(0, '评论成功')


# 用户电影台词评论接口
class LinesCommentAPIView(APIView):
    """用户电影台词评论接口"""
    def post(self, request, *args, **kwargs):
        print(request.data)
        user_id = request.data.get('user_id')
        lines_id = request.data.get('lines_id')
        content = request.data.get('context')

        models.LinesComment.objects.create(user_id=user_id, lines_id=lines_id, content=content)

        return APIResponse(0, '评论成功')


# 用户点赞收藏标识接口
class IsUpAndIsFavAPIView(APIView):
    """用户点赞收藏标识接口"""
    def post(self, request, *args, **kwargs):
        movie_id = request.data.get('movie_id')
        user_id = request.data.get('user_id')

        fav_obj = models.Favorite.objects.filter(user_id=user_id, movie_id=movie_id).first()
        up_obj = models.UpOrDown.objects.filter(user_id=user_id, movie_id=movie_id).first()

        if fav_obj:
            fav_msg = '已收藏'
        else:
            fav_msg = '收藏'

        if up_obj:
            up_msg = '已点赞'
        else:
            up_msg = '点赞'

        return Response(data={'fav_msg': fav_msg, 'up_msg': up_msg})


# 用户收藏接口
class FavoriteAPIView(APIView):
    """用户收藏接口"""
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        print(user_id)
        fav_list = models.Favorite.objects.filter(user_id=user_id).all()

        fav_ser = serializers.FavoriteModelSerializer(fav_list, many=True, context={'request': request}).data

        return Response(data=fav_ser)


# 重置密码接口
class ResetPasswordAPIVIew(APIView):
    """重置密码接口"""
    def post(self, request, *args, **kwargs):
        data = request.data

        user_ser = serializers.ResetPasswordModelSerializer(data=data)
        user_ser.is_valid(raise_exception=True)

        return APIResponse(results='重置密码成功')


