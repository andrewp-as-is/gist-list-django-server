__all__ = ['ApiGraphqlUserFollowersResponseJob']

from django.db import models

class ApiGraphqlUserFollowersResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
