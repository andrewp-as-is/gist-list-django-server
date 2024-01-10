__all__ = ['Tag',]

from django.db import models

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(unique=True,max_length=255)

    class Meta:
        managed = False
