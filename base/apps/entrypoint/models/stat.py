__all__ = ['Stat',]

from django.db import models

class Stat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    count = models.IntegerField()
    avg_duration = models.IntegerField()
    min_duration = models.IntegerField()
    max_duration = models.IntegerField()

    class Meta:
        managed = False
