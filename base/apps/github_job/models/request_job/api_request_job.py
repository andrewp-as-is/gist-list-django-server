__all__ = ['ApiRequestJob']

from django.db import models

class ApiRequestJob(models.Model):
    domain = models.TextField()
    url = models.TextField(unique=True)
    response_relpath = models.TextField()
    priority = models.IntegerField()

    class Meta:
        managed = False
