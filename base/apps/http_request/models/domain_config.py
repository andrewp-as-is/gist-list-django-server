__all__ = ['DomainConfig',]

from django.db import models

class DomainConfig(models.Model):
    domain = models.TextField(unique=True)
    attempts_limit = models.IntegerField()
    requests_limit = models.IntegerField()
