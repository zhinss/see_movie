from django.db import models
from utils.models import BaseModel
from user.models import MyUser


# 订单表
class Order(BaseModel):
    """订单表"""
    status_choices = (
        (0, '未支付'),
        (1, '已支付'),
        (2, '已取消'),
        (3, '超时取消'),
    )

    subject = models.CharField(max_length=150, verbose_name='订单标题')
    buy_time = models.IntegerField(verbose_name='购买时长')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价', default=0)
    out_trade_no = models.CharField(max_length=64, verbose_name='订单号', unique=True)
    trade_no = models.CharField(max_length=64, null=True, verbose_name='流水号')
    order_status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name='订单状态')
    pay_time = models.DateTimeField(null=True, verbose_name='支付时间')
    user = models.ForeignKey(to=MyUser, on_delete=models.DO_NOTHING, db_constraint=False, verbose_name='下单用户')

    class Meta:
        verbose_name = '订单记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s - ￥%s" % (self.subject, self.total_amount)


# 订单详情
# class OrderDetail(BaseModel):
#     """订单详情"""
#     order = models.ForeignKey(to=Order, on_delete=models.CASCADE, db_constraint=False, verbose_name="订单")
#