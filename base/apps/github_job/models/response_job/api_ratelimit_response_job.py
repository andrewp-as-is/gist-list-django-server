__all__ = ['ApiRatelimitResponseJob']

from django.db import models

class ApiRatelimitResponseJob(models.Model):
    response_id = models.IntegerField()

    class Meta:
        managed = False
