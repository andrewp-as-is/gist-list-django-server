__all__ = ['Cursor',]

from django.db import models

class Cursor(models.Model):
    name = models.TextField(unique=True)
    row_id = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('name', )
