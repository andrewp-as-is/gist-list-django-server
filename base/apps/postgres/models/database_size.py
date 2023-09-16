__all__ = ['DatabaseSize',]

from django.db import models

class DatabaseSize(models.Model):
    name = models.TextField(unique=True)
    size = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('name', )
