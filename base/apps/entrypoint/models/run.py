__all__ = ['Run',]

from django.db import models

class Run(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    started_at = models.IntegerField()
    finished_at = models.IntegerField(null=True)

    class Meta:
        managed = False
