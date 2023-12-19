__all__ = ['UserRefreshReport']

import time

from django.db import models

class UserRefreshReport(models.Model):

    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    viewer = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    duration = models.FloatField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
