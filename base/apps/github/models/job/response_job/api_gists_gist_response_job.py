__all__ = ['ApiGistsGistResponseJob']

from django.db import models

class ApiGistsGistResponseJob(models.Model):
    response_id = models.IntegerField()
    gist_id = models.TextField()

    class Meta:
        managed = False
