# Generated by Django 2.0.7 on 2019-12-24 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20191224_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='lines',
            name='movie_name',
            field=models.CharField(default='这个杀手不太冷', max_length=32, verbose_name='电影'),
        ),
    ]
