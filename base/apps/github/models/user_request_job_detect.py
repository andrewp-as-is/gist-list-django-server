__all__ = ['UserRequestJobDetect']

from django.db import models

class UserRequestJobDetect(models.Model):
    url = models.TextField()
    user_id = models.IntegerField()

    class Meta:
        managed = False

