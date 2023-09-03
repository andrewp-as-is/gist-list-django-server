__all__ = ['Info']

from django.db import models

class Info(models.Model):
    name = models.TextField(unique=True)
    called_at = models.IntegerField(null=True)

    class Meta:
        managed = False
        verbose_name_plural = "Info"

