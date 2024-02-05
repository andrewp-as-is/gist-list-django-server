__all__ = ['VacuumFullLock',]

from django.db import models

class VacuumFullLock(models.Model):
    id = models.AutoField(primary_key=True)
    schemaname = models.TextField()
    tablename = models.TextField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
        unique_together = ('schemaname', 'tablename',)
