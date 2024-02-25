__all__ = ['CallLog',]

from django.db import models

class CallLog(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    created_at = models.IntegerField()

    class Meta:
        managed = False
