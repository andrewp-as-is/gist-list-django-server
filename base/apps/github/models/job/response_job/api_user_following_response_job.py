__all__ = ['ApiUserFollowingResponseJob']

from django.db import models

class ApiUserFollowingResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
