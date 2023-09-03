__all__ = ['Useragent']

from django.db import models

class Useragent(models.Model):
    useragent = models.TextField(unique=True)

    class Meta:
        managed = False
