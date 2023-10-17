__all__ = ['Incident',]

from django.db import models

class Incident(models.Model):
    message = models.CharField(max_length=255)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-timestamp', )
