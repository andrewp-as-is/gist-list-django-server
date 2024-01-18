__all__ = ['Config',]

from django.db import models

class Config(models.Model):
    id = models.AutoField(primary_key=True)
    schemaname = models.CharField(max_length=255)
    tablename = models.CharField(max_length=255)
    count = models.IntegerField()

    class Meta:
        managed = False
        unique_together = ('schemaname', 'tablename',)
