__all__ = ['ApiUserFollowersResponseJobSnapshot']

from django.db import models

class ApiUserFollowersResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
