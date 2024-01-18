__all__ = ['BackupJob',]

from django.db import models

class BackupJob(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
