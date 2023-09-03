__all__ = ['ApiGraphqlRatelimitResponseJob']

from django.db import models

class ApiGraphqlRatelimitResponseJob(models.Model):
    response_id = models.IntegerField()

    class Meta:
        managed = False
