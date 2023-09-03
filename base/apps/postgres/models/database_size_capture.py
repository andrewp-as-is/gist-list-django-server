__all__ = ['DatabaseSizeCapture',]

from django.db import models

class DatabaseSizeCapture(models.Model):
    name = models.TextField()
    size = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('name', )
