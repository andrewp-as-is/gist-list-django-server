__all__ = ['Config']

from django.db import models

class Config(models.Model):
    name = models.CharField(max_length=255)
    output = models.BooleanField()

    class Meta:
        managed = False
        ordering = ('name',)
