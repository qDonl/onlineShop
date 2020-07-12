from django.db import models


class BaseModel(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加事件")

    class Meta:
        abstract = True
