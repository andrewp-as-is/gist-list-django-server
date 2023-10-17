__all__ = ['User',]

from django.db import models

from base.apps.github.models import AbstractUser

class User(AbstractUser):
    refresh_timestamp = models.IntegerField()

    class Meta:
        managed = False
