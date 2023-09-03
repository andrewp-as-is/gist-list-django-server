__all__ = ['Repeat',]

from django.db import models

class Repeat(models.Model):
    name = models.TextField(unique=True)
    seconds = models.IntegerField()

    class Meta:
        managed = False
        verbose_name_plural = "Repeat"
