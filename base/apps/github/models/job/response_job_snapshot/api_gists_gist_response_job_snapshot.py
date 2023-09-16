__all__ = ['ApiGistsGistResponseJobSnapshot']

from django.db import models

class ApiGistsGistResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    gist_id = models.TextField()

    class Meta:
        managed = False
