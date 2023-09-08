__all__ = ['CallInfo']

from django.db import models

class CallInfo(models.Model):
    name = models.TextField(unique=True)
    success = models.BooleanField()
    duration = models.FloatField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        verbose_name_plural = "call_info"

