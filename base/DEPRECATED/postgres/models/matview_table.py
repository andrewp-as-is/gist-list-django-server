__all__ = ['MatviewTable',]

from django.db import models

class MatviewTable(models.Model):
    schema = models.TextField()
    table = models.TextField()

    class Meta:
        managed = False
        ordering = ('schema', 'table')
