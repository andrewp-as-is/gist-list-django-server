__all__ = ["ApiResponseTime"]

from django.db import models


class ApiResponseTime(models.Model):
    url = models.TextField(unique=True)
    created_at = models.FloatField()

    class Meta:
        managed = False
