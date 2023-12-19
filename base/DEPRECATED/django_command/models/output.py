__all__ = ['Output']

from django.db import models

class Output(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-created_at',)
