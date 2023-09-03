__all__ = ['Incident',]

from django.db import models

class Incident(models.Model):
    message = models.TextField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-timestamp', )
