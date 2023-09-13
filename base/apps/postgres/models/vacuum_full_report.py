__all__ = ['VacuumFullReport']

from django.db import models

class VacuumFullReport(models.Model):
    schemaname = models.TextField()
    tablename = models.TextField()
    duration = models.FloatField()
    size_before = models.TextField()
    size_after = models.TextField()
    timestamp = models.TextField()

    class Meta:
        managed = False
        unique_together = [('schemaname','tablename',)]

