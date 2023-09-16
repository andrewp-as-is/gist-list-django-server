__all__ = ['ApiViewerGistsStarredResponseJob']

from django.db import models

class ApiViewerGistsStarredResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
