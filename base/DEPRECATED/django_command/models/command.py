__all__ = ['Command']

from django.db import models

class Command(models.Model):
    name = models.CharField(unique=True,max_length=255)
    app = models.CharField(max_length=255)

    class Meta:
        managed = False
