__all__ = ["ApiCoreRequestJob"]

from django.db import models


class ApiCoreRequestJob(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField(unique=True)
    disk_relpath = models.TextField()

    class Meta:
        managed = False  # VIEW
