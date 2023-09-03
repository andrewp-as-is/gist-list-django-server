__all__ = ['ApiUserGistsResponseJob']

from django.db import models

class ApiUserGistsResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
