__all__ = ['ApiGraphqlUserGistsResponseJobSnapshot']

from django.db import models

class ApiGraphqlUserGistsResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
