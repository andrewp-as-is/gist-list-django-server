__all__ = ['Queue',]

from django.db import models

class Queue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
