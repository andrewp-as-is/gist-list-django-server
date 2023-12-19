__all__ = ["ApiCoreRequestJob"]

from django.db import models


class ApiCoreRequestJob(models.Model):
    url = models.TextField(unique=True)
    disk_relpath = models.TextField()

    class Meta:
        managed = False  # VIEW
