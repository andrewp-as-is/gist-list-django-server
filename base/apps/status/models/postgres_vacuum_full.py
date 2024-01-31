__all__ = ['PostgresVacuumFull',]

from django.db import models

class PostgresVacuumFull(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.CharField(max_length=256)
    duration = models.FloatField()

    class Meta:
        managed = False
