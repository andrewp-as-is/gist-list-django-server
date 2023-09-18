__all__ = ['Table']

from django.db import models


class Table(models.Model):
    schemaname = models.TextField()
    tablename = models.TextField()

    class Meta:
        managed = False
