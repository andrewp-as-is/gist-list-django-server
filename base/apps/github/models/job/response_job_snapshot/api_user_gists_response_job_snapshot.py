__all__ = ['ApiUserGistsResponseJobSnapshot']

from django.db import models

class ApiUserGistsResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
