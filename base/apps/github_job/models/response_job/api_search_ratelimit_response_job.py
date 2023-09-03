__all__ = ['ApiSearchRatelimitResponseJob']

from django.db import models

class ApiSearchRatelimitResponseJob(models.Model):
    response_id = models.IntegerField()

    class Meta:
        managed = False
