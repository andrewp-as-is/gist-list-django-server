__all__ = ['DomainConfig',]

from django.db import models

class DomainConfig(models.Model):
    domain = models.CharField(unique=True,max_length=255)
    attempts_limit = models.IntegerField()
    requests_limit = models.IntegerField()
