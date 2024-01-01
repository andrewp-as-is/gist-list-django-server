__all__ = ['Incident',]

from django.db import models

class Incident(models.Model):
    id = models.IntegerField(primary_key=True)
    message = models.CharField(max_length=255)
    created_at = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-created_at', )
