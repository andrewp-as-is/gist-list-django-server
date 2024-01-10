__all__ = ['QueryStat',]

from django.db import models

class QueryStat(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.TextField()
    type = models.CharField(max_length=255)
    count = models.FloatField()
    avg_duration = models.IntegerField()
    min_duration = models.FloatField()
    max_duration = models.FloatField()

    class Meta:
        managed = False
        ordering = ('query', )
