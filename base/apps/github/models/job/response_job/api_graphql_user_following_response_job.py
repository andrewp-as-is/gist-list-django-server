__all__ = ['ApiGraphqlUserFollowingResponseJob']

from django.db import models

class ApiGraphqlUserFollowingResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
