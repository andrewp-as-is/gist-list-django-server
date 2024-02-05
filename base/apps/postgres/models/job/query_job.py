__all__ = ['QueryJob',]

from django.db import models

class QueryJob(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.TextField()

    class Meta:
        managed = False
        ordering = ('query', )
