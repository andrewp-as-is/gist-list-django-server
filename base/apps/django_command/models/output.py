__all__ = ['Output']

from django.db import models

from base.utils import get_timestamp

class Output(models.Model):
    name = models.TextField()
    output = models.TextField()
    timestamp = models.IntegerField(default=get_timestamp)

    class Meta:
        managed = False
        ordering = ('-timestamp', )
        verbose_name_plural = "Output"
