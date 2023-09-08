__all__ = ['RefreshInfo',]

from django.db import models

class RefreshInfo(models.Model):
    regclass = models.TextField()
    duration = models.FloatField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-timestamp', )
