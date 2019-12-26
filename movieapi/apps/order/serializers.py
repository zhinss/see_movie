import time

from rest_framework import serializers
from django.conf import settings

from order import models
from libs.iPay import alipay, alipay_gateway


# 支付序列化类
class PayModelSerializer(serializers.ModelSerializer):
    """支付序列化类"""
    class Meta:
        model = models.Order
        fields = ['subject', 'buy_time', 'total_amount']

    # 全局钩子
    def validate(self, attrs):
        # 生成订单号
        order_no = self._get_order_no()
        # 订单名
        subject = attrs.get('subject')
        # 获取商品价格
        total_amount = attrs.get('total_amount')

        order_string = alipay.api_alipay_trade_page_pay(
            # 订单号
            out_trade_no=order_no,
            # 订单价格
            total_amount=float(total_amount),
            # 订单名
            subject=subject,
            # 前台回调接口
            return_url=settings.RETURN_URL,
            # 后台异步回调接口(8次)
            notify_url=settings.NOTIFY_URL  # this is optional
        )

        # 生成支付链接
        pay_url = alipay_gateway + order_string

        # 将支付链接保存在serializer对象中
        self.pay_url = pay_url

        # 添加订单表需要的额外字段
        attrs['out_trade_no'] = order_no
        attrs['user'] = self.context.get('request').user

        return attrs

    # 生成订单号
    def _get_order_no(self):
        no = f'{time.time()}'
        return no.replace('.', '', 1)
