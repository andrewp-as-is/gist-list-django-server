__all__ = ['OutputStat']

from django.db import models

class OutputStat(models.Model):
    name = models.CharField(max_length=255)
    count = models.IntegerField()
    avg_size = models.IntegerField()
    min_size = models.IntegerField()
    max_size = models.IntegerField()
    total_size = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('name',)
