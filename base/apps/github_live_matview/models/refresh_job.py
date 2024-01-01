__all__ = ['RefreshJob']

from django.db import models

class RefreshJob(models.Model):
    id = models.IntegerField(primary_key=True)
    matviewname = models.IntegerField(unique=True)
    created_at = models.IntegerField()

    class Meta:
        managed = False
