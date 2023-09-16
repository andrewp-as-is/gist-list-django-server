__all__ = ['ApiGraphqlViewerGistsResponseJobSnapshot']

from django.db import models

class ApiGraphqlViewerGistsResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
