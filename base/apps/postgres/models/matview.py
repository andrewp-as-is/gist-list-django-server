__all__ = ['Matview',]

from django.db import models

class Matview(models.Model):
    id = models.AutoField(primary_key=True)
    schemaname = models.TextField()
    matviewname = models.TextField()
    refreshed_at = models.FloatField()

    class Meta:
        managed = False
        ordering = ('schemaname','matviewname',)
        unique_together = ('schemaname', 'matviewname',)
