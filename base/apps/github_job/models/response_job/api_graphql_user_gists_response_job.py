__all__ = ['ApiGraphqlUserGistsResponseJob']

from django.db import models

class ApiGraphqlUserGistsResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
