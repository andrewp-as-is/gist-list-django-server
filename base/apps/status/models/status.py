__all__ = ['Status',]

from django.db import models

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    postgres_vacuum_full = models.BooleanField(null=True)
    refreshed_at = models.IntegerField()

    class Meta:
        managed = False
