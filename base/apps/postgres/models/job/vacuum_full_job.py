__all__ = ['VacuumFullJob',]

from django.db import models

class VacuumFullJob(models.Model):
    id = models.AutoField(primary_key=True)
    schemaname = models.TextField()
    tablename = models.TextField()

    class Meta:
        managed = False
        ordering = ('schemaname','tablename',)
        unique_together = ('schemaname', 'tablename',)
