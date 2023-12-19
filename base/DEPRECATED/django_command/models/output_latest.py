__all__ = ['OutputLatest']

from django.db import models

class OutputLatest(models.Model):
    name = models.CharField(unique=True,max_length=255)
    created_at = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('name', )
