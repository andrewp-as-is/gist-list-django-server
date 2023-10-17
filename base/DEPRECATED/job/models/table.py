__all__ = ['Table',]

from django.db import models

class Table(models.Model):
    schemaname = models.CharField(max_length=255)
    tablename = models.CharField(max_length=255)
    tuples = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('schemaname','tablename',)
