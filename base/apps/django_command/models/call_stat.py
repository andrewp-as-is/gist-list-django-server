__all__ = ['CallStat']

from django.db import models

class CallStat(models.Model):
    name = models.TextField(unique=True)
    calls_count = models.IntegerField()

    class Meta:
        managed = False
        verbose_name_plural = "call_stat"

