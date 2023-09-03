__all__ = ['Tag',]

from django.db import models

class Tag(models.Model):
    slug = models.TextField(unique=True)

    class Meta:
        managed = False
