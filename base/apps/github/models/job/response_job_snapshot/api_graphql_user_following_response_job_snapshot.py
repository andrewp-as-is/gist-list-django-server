__all__ = ['ApiGraphqlUserFollowingResponseJobSnapshot']

from django.db import models

class ApiGraphqlUserFollowingResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
