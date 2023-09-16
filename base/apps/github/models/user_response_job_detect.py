__all__ = ['UserResponseJobDetect']

from django.db import models

class UserResponseJobDetect(models.Model):
    viewname = models.TextField()
    user_id = models.IntegerField()

    class Meta:
        managed = False

