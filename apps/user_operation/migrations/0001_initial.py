# Generated by Django 2.2.2 on 2020-04-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加事件')),
                ('province', models.CharField(blank=True, max_length=100, null=True, verbose_name='省份')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='城市')),
                ('district', models.CharField(blank=True, max_length=100, null=True, verbose_name='区域')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='详细地址')),
                ('signer_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='签收人')),
                ('signer_mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话')),
            ],
            options={
                'verbose_name': '收货地址',
                'verbose_name_plural': '收货地址',
            },
        ),
        migrations.CreateModel(
            name='UserFav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加事件')),
            ],
            options={
                'verbose_name': '用户收藏',
                'verbose_name_plural': '用户收藏',
            },
        ),
        migrations.CreateModel(
            name='UserLeavingMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加事件')),
                ('message_type', models.IntegerField(choices=[(1, '留言'), (2, '投诉'), (3, '询问'), (4, '售后'), (5, '求购')], default=1, help_text='留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)', verbose_name='留言类型')),
                ('subject', models.CharField(blank=True, max_length=100, null=True, verbose_name='主题')),
                ('message', models.TextField(default='', verbose_name='留言内容')),
                ('file', models.FileField(upload_to='message/images/', verbose_name='上传的文件')),
            ],
            options={
                'verbose_name': '用户留言',
                'verbose_name_plural': '用户留言',
            },
        ),
    ]