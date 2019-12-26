import datetime
from dateutil.relativedelta import relativedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from order import serializers
from libs.iPay import alipay
from order import models
from utils.logging import logger


# 支付接口
class PayAPIView(APIView):
    """支付接口"""
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = serializers.PayModelSerializer(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.pay_url)


# 支付成功回调接口
class PaySuccessAPIView(APIView):
    """支付成功回调接口"""
    # 异步支付宝回调接口：公网下才能验证
    def post(self, request, *args, **kwargs):
        data = request.data.dict()  # 回调参数，是QueryDict类型，不能直接调用pop方法
        sign = data.pop('sign')  # 签名
        out_trade_no = data.get('out_trade_no')  # 订单号
        result = alipay.verify(data, sign)
        if result and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            try:
                order = models.Order.objects.get(out_trade_no=out_trade_no)
                if order.order_status != 1:
                    order.order_status = 1
                    order.save()
                    logger.warning('%s订单完成支付' % out_trade_no)
                return Response('success')
            except:
                pass
        return Response('failed')

    # 重点：要不要做登录认证，不需要：订单号可以获取你所需要的所有信息、回调参数有自己的安全校验、支付宝永远不可能通过token
    def patch(self, request, *args, **kwargs):
        # print(request.query_params)
        data = request.query_params.dict()
        sign = data.pop('sign')
        result = alipay.verify(data, sign)
        if result:
            # 一般不在同步回调直接操作订单状态
            pass
            order = models.Order.objects.filter(out_trade_no=data.get('out_trade_no')).first()

            # 判断当前用户是否是会员
            if not order.user.is_vip:
                order.user.is_vip = True
                order.user.vip_expire_date = datetime.date.today() + relativedelta(months=+order.buy_time)
                order.user.vip_time = str(datetime.date.today() + relativedelta(months=+order.buy_time))
                order.user.save()
            else:
                order.user.vip_time = str(order.user.vip_expire_date + relativedelta(months=+order.buy_time))[:10]
                order.user.vip_expire_date = order.user.vip_expire_date + relativedelta(months=+order.buy_time)
                order.user.save()

        return Response('同步回调完成')
