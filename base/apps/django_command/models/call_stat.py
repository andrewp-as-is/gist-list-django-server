__all__ = ['CallStat']

from django.db import models

class CallStat(models.Model):
    name = models.CharField(unique=True,max_length=255)
    calls_count = models.IntegerField()

    class Meta:
        managed = False
