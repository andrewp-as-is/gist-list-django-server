__all__ = ['RefreshStat',]

from django.db import models

class RefreshStat(models.Model):
    schemaname = models.TextField()
    matviewname = models.TextField()
    count = models.IntegerField()
    avg_duration = models.FloatField()
    min_duration = models.FloatField()
    max_duration = models.FloatField()

    class Meta:
        managed = False
        ordering = ('schemaname','matviewname',)
        unique_together = [('schemaname','matviewname',)]

