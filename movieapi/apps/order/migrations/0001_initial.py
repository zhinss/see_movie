# Generated by Django 2.0.7 on 2019-12-25 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=150, verbose_name='订单标题')),
                ('buy_time', models.IntegerField(verbose_name='购买时长')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='订单总价')),
                ('out_trade_no', models.CharField(max_length=64, unique=True, verbose_name='订单号')),
                ('trade_no', models.CharField(max_length=64, null=True, verbose_name='流水号')),
                ('order_status', models.SmallIntegerField(choices=[(0, '未支付'), (1, '已支付'), (2, '已取消'), (3, '超时取消')], default=0, verbose_name='订单状态')),
                ('pay_time', models.DateTimeField(null=True, verbose_name='支付时间')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='下单用户')),
            ],
            options={
                'verbose_name': '订单记录',
                'verbose_name_plural': '订单记录',
            },
        ),
    ]
