__all__ = ['RefreshStat',]

from django.db import models

class RefreshStat(models.Model):
    regclass = models.TextField(unique=True)
    avg_duration = models.FloatField()
    min_duration = models.FloatField()
    max_duration = models.FloatField()

    class Meta:
        managed = False
        ordering = ('regclass', )
