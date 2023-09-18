__all__ = ['RefreshScheduler',]

from django.db import models

class RefreshScheduler(models.Model):
    schemaname = models.TextField()
    matviewname = models.TextField()
    seconds = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('schemaname','matviewname',)
        unique_together = [('schemaname', 'matviewname',)]
