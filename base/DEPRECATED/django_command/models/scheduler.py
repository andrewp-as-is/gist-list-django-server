__all__ = ['Scheduler',]

from django.db import models

class Scheduler(models.Model):
    name = models.CharField(unique=True,max_length=255)
    seconds = models.IntegerField()

    class Meta:
        managed = False
