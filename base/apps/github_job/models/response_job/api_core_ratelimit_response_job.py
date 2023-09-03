__all__ = ['ApiCoreRatelimitResponseJob']

from django.db import models

class ApiCoreRatelimitResponseJob(models.Model):
    response_id = models.IntegerField()

    class Meta:
        managed = False
