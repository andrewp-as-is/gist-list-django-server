__all__ = ['TableSize',]

from django.db import models

class TableSize(models.Model):
    regclass = models.TextField()
    schemaname = models.TextField()
    tablename = models.TextField()
    size = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('regclass', )
