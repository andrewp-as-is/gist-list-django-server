__all__ = ['ResponseJob',]

from django.db import models


class ResponseJob(models.Model):
    response_id = models.IntegerField()

    class Meta:
        managed = False
