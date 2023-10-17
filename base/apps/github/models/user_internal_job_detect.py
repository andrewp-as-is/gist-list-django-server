__all__ = ['UserInternalJobDetect']

from django.db import models

class UserInternalJobDetect(models.Model):
    user_id = models.IntegerField()

    class Meta:
        managed = False

