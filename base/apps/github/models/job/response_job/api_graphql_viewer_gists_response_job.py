__all__ = ['ApiGraphqlViewerGistsResponseJob']

from django.db import models

class ApiGraphqlViewerGistsResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
