__all__ = ['Output']

from django.db import models

from base.utils import get_timestamp

class Output(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    timestamp = models.IntegerField(default=get_timestamp)

    class Meta:
        managed = False
        ordering = ('-timestamp',)
