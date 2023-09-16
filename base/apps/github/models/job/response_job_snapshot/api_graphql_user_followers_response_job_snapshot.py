__all__ = ['ApiGraphqlUserFollowersResponseJobSnapshot']

from django.db import models

class ApiGraphqlUserFollowersResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
