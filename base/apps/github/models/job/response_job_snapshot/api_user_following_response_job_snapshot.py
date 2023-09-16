__all__ = ['ApiUserFollowingResponseJobSnapshot']

from django.db import models

class ApiUserFollowingResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
