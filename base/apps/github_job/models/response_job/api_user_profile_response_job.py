__all__ = ['ApiUserProfileResponseJob']

from django.db import models

class ApiUserProfileResponseJob(models.Model):
    response_id = models.IntegerField()
    user_id = models.TextField(null=True)

    class Meta:
        managed = False
