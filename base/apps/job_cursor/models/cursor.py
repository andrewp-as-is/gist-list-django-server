__all__ = ['Cursor',]

from django.db import models

class Cursor(models.Model):
    regclass = models.TextField(unique=True)
    job_id = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('regclass', )
