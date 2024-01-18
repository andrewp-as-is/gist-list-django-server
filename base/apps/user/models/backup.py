__all__ = ['Backup',]

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Backup(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    description = models.TextField(null=True)
    filename_list = ArrayField(models.TextField())
    created_at = models.IntegerField()

    class Meta:
        managed = False
