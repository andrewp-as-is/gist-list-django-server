__all__ = ['RefreshLock',]

from django.db import models

class RefreshLock(models.Model):
    id = models.AutoField(primary_key=True)
    schemaname = models.TextField()
    matviewname = models.TextField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
        unique_together = ('schemaname', 'matviewname',)
