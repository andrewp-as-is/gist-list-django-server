__all__ = ['Useragent']

from django.db import models

class Useragent(models.Model):
    useragent = models.CharField(unique=True,max_length=255)

    class Meta:
        managed = False
