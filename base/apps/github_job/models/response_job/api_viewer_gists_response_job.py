__all__ = ['ApiViewerGistsResponseJob']

from django.db import models

class ApiViewerGistsResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
