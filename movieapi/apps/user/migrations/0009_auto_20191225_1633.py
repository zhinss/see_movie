# Generated by Django 2.0.7 on 2019-12-25 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20191225_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='nick_name',
            field=models.CharField(blank=True, default='用户20191225163326', max_length=32, verbose_name='昵称'),
        ),
    ]
