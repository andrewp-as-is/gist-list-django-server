__all__ = ['CommandIgnore']

from django.db import models

class CommandIgnore(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        managed = False

