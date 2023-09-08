__all__ = ['Matview',]

from django.db import models

class Matview(models.Model):
    regclass = models.TextField(unique=True)
    duration = models.FloatField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('regclass', )
