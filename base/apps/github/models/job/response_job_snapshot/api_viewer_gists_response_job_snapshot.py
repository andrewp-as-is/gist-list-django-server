__all__ = ['ApiViewerGistsResponseJobSnapshot']

from django.db import models

class ApiViewerGistsResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
