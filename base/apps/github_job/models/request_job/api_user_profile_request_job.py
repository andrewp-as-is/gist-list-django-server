__all__ = ['ApiUserProfileRequestJob']

from django.db import models

class ApiUserProfileRequestJob(models.Model):
    user_id = models.TextField()

    class Meta:
        managed = False
