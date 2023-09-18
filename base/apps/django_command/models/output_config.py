__all__ = ['OutputConfig']

from django.db import models

class OutputConfig(models.Model):
    name = models.CharField(max_length=255)
    save = models.BooleanField()

    class Meta:
        managed = False
        ordering = ('name',)
