__all__ = ['Matview',]

from django.db import models

class Matview(models.Model):
    schemaname = models.TextField()
    tablename = models.TextField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('schemaname','tablename',)
        unique_together = [('schemaname','tablename',)]

