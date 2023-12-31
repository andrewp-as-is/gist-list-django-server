__all__ = ['UserRefreshStat']

import time

from django.db import models

class UserRefreshStat(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    count = models.IntegerField()
    avg_duration = models.FloatField()
    min_duration = models.FloatField()
    max_duration = models.FloatField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
