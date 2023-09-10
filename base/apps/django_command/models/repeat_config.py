__all__ = ['RepeatConfig',]

from django.db import models

class RepeatConfig(models.Model):
    name = models.CharField(unique=True,max_length=255)
    seconds = models.IntegerField()

    class Meta:
        managed = False
