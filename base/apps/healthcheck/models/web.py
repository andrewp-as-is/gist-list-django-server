__all__ = ['Web',]

from django.db import models

class Web(models.Model):
    url = models.TextField(unique=True)

    class Meta:
        managed = False
        ordering = ('url', )
