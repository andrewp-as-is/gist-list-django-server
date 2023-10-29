__all__ = ["ApiCoreRequestJob"]

from django.db import models


class ApiCoreRequestJob(models.Model):
    url = models.TextField(unique=True)
    disk_disk_path = models.TextField()

    class Meta:
        managed = False
