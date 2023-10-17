__all__ = ['Procedure',]

from django.db import models

class Procedure(models.Model):
    schemaname = models.CharField(max_length=255)
    proname = models.CharField(max_length=255)

    class Meta:
        managed = False
        ordering = ('schemaname','proname',)
