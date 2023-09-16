__all__ = ['Relation',]

from django.db import models

class Relation(models.Model):
    schemaname = models.CharField(max_length=255)
    tablename = models.CharField(max_length=255)
    tuples = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('schemaname','tablename',)
