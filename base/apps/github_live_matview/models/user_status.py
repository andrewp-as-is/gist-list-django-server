__all__ = [
    "UserStatus",
]

from django.contrib.postgres.fields import ArrayField
from django.db import models


class UserStatus(models.Model):
    id = models.AutoField(primary_key=True)
    user_id  = models.IntegerField(unique=True)
    matview_list  = ArrayField(models.IntegerField())

    class Meta:
        managed = False
