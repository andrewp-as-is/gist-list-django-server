__all__ = ['SqlStat',]

from django.db import models

class SqlStat(models.Model):
    sql = models.TextField(unique=True)
    count = models.IntegerField()
    avg_duration = models.FloatField()
    min_duration = models.FloatField()
    max_duration = models.FloatField()

    class Meta:
        managed = False
        ordering = ('sql',)

