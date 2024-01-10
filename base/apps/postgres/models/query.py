__all__ = ['Query',]

from django.db import models

class Query(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.TextField()
    duration = models.FloatField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-created_at', )
