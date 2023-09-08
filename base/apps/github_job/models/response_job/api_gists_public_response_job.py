__all__ = ['ApiGistsPublicResponseJob']

from django.db import models

class ApiGistsPublicResponseJob(models.Model):
    response_id = models.IntegerField()

    class Meta:
        managed = False
