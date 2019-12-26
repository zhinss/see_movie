# Generated by Django 2.0.7 on 2019-12-24 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20191217_0847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=256, verbose_name='台词')),
                ('order', models.IntegerField(verbose_name='显示顺序')),
            ],
            options={
                'verbose_name': '电影台词',
                'verbose_name_plural': '电影台词',
            },
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(blank=True, upload_to='movie/%Y/%m', verbose_name='电影图'),
        ),
    ]