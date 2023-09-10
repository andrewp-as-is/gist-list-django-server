__all__ = ['Cursor',]

from django.db import models

class Cursor(models.Model):
    name = models.CharField(unique=True,max_length=255)
    row_id = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('name', )
