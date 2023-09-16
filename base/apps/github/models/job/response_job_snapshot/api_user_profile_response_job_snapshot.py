__all__ = ['ApiUserProfileResponseJobSnapshot']

from django.db import models

class ApiUserProfileResponseJobSnapshot(models.Model):
    response_id = models.IntegerField()
    user_id = models.TextField(null=True)

    class Meta:
        managed = False
