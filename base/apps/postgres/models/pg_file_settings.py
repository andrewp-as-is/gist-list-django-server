__all__ = ['PgFileSettings',]

from django.db import models

class PgFileSettings(models.Model):
    sourcefile = models.TextField()
    sourceline = models.IntegerField()
    seqno = models.IntegerField()
    name = models.TextField()
    setting = models.TextField()
    applied = models.IntegerField()
    error = models.BooleanField()

    class Meta:
        managed = False
        ordering = ('sourcefile','sourceline',)
