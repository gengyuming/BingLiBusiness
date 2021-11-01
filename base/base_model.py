from django.db import models


class BaseModel(models.Model):
    """
    表公共字段
    """
    creator = models.CharField(verbose_name="创建人", max_length=32, blank=True, null=True)
    updater = models.CharField(verbose_name="更新人", max_length=32, blank=True, null=True)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    is_delete = models.CharField(max_length=2, default='N', null=True)

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'base_model'
