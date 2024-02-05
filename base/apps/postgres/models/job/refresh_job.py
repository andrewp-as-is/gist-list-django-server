__all__ = ['RefreshJob',]

from django.db import models

class RefreshJob(models.Model):
    id = models.AutoField(primary_key=True)
    schemaname = models.TextField()
    matviewname = models.TextField()

    class Meta:
        managed = False
        unique_together = ('schemaname', 'matviewname',)
