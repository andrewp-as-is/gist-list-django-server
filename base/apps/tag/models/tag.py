__all__ = ['Tag',]

from django.db import models

class Tag(models.Model):
    slug = models.CharField(unique=True,max_length=255)

    class Meta:
        managed = False
