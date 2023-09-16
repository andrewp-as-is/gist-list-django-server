__all__ = ['ApiViewerGistsStarredResponseJobSnapshot']

from django.db import models

class ApiViewerGistsStarredResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
