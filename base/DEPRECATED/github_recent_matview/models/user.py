__all__ = [
    "User",
]

from django.db import models

from base.apps.github.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
