# Generated by Django 2.2.2 on 2020-05-08 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20200419_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='post_script',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='订单留言'),
        ),
    ]
