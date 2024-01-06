__all__ = [
    "User",
]

from django.db import models

from base.apps.github.models import AbstractUser


class User(AbstractUser):
    id = models.IntegerField(primary_key=True)
    refreshed_at = models.IntegerField(null=True)
    secret_refreshed_at = models.IntegerField(null=True)

    class Meta:
        managed = False
