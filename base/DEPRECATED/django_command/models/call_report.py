__all__ = ['CallReport']

from django.db import models

class CallReport(models.Model):
    name = models.CharField(max_length=255)
    duration = models.FloatField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
