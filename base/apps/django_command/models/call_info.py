__all__ = ['CallInfo']

from django.db import models

class CallInfo(models.Model):
    name = models.CharField(max_length=255)
    duration = models.FloatField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
