import re

from django.conf import settings
from django.core.cache import cache
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from user import models
from libs.send_email import send_email
from movie.models import Tag, Movie


# 注册序列化类
class RegisterModelSerializer(serializers.ModelSerializer):
    """注册序列化类"""

    code = serializers.CharField(max_length=settings.CODE_LEN, min_length=settings.CODE_LEN, write_only=True)

    class Meta:
        model = models.MyUser
        fields = ['username', 'password', 'phone', 'code', 'email']
        extra_kwargs = {
            'username': {
                'min_length': 2,
                'max_length': 11,
            },
            'password': {
                'min_length': 6,
                'max_length': 16,
                'write_only': True,
            },
            'phone': {
                'min_length': 11,
                'max_length': 11,
            }
        }

    # 局部钩子
    def validated_phone(self, value):
        """校验手机号"""
        if not re.match(r'^1[3-9][0-9]{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validated_email(self, value):
        """校验手机号"""
        if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', value):
            raise serializers.ValidationError('邮箱格式错误')
        return value

    # 全局钩子校验验证码
    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.pop('code')
        old_code = cache.get(settings.SMS_CACHE_KEY % phone)

        if code != old_code:
            raise serializers.ValidationError({'code': '验证码错误'})

        return attrs

    # 重写create方法保存加密的密码
    def create(self, validated_data):
        user = models.MyUser.objects.create_user(**validated_data)
        return user


# 登陆序列化类
class LoginModelSerializer(serializers.ModelSerializer):
    """登陆序列化类"""
    username = serializers.CharField(min_length=2, max_length=11, write_only=True)
    password = serializers.CharField(min_length=6, max_length=16, write_only=True)

    class Meta:
        model = models.MyUser
        fields = ['username', 'password']

    # 全局钩子验证用户签发token
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = models.MyUser.objects.filter(username=username).first()

        if not user:
            raise serializers.ValidationError({"username": '用户未注册'})

        if not user.check_password(password):
            raise serializers.ValidationError({"username": '密码错误'})

        # 传入user对象获取payload对象
        payload = jwt_payload_handler(user)
        # 传入payload对象获取token
        token = jwt_encode_handler(payload)

        self.token = token
        self.user = user

        return attrs


# 用户信息序列化类
class InfoModelSerializer(serializers.ModelSerializer):
    """用户信息序列化类"""
    class Meta:
        model = models.MyUser
        fields = [
            'username',
            'email',
            'phone',
            'is_vip',
            'is_active',
            'fav_type',
            'image',
            'vip_time',
        ]


# 修改用户信息序列化类
# class ChangeInfoModelSerializer(serializers.ModelSerializer):
#     """修改用户信息序列化类"""
#     class Meta:
#         model = models.MyUser
#         fields = ['username', 'email', 'phone', 'fav_type']
#
#     # 全局钩子
#     def validate(self, attrs):
#         attrs.pop('is_vip')
#         attrs.pop('is_active')
#         attrs.pop('image')
#         fav_type = attrs.pop('fav_type')
#
#         tag_obj = Tag.objects.filter(name=fav_type)
#
#         attrs['fav_type'] = tag_obj
#
#         return attrs
#
#     def update(self, instance, validated_data):
#         username = validated_data.pop('username')
#
#         row = instance.update(**validated_data)
#
#         return instance


# 电影序列化类
class MovieModelSerializer(serializers.ModelSerializer):
    """电影序列化类"""

    class Meta:
        model = Movie
        fields = ['pk', 'image', 'name', 'movie_type']


# 用户收藏序列化类
class FavoriteModelSerializer(serializers.ModelSerializer):
    """用户收藏序列化类"""
    movie = MovieModelSerializer()

    class Meta:
        model = models.Favorite
        fields = ['movie']


# 重置密码序列化类
class ResetPasswordModelSerializer(serializers.ModelSerializer):
    """重置密码序列化类"""
    username = serializers.CharField(min_length=2, max_length=11, write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = models.MyUser
        fields = ['username', 'email']

    # 局部钩子验证用户是存在
    def validated_username(self, value):

        user = models.MyUser.objects.filter(username=value)

        if not user:
            raise serializers.ValidationError('用户未注册')

        return value

    # 全局钩子
    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        user = models.MyUser.objects.filter(username=username).first()

        if user.email != email:
            raise serializers.ValidationError({'username': '用户邮箱错误'})

        # 发送邮箱
        send_email(email, username)

        # 修改密码
        new_password = f'{username}123'
        user.set_password(new_password)
        user.save()

        return attrs
