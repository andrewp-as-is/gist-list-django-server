__all__ = ['ApiUserFollowersResponseJob']

from django.db import models

class ApiUserFollowersResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
