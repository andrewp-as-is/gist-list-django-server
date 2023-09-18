__all__ = ['Rule']

from django.db import models


class Rule(models.Model):
    schemaname = models.TextField()
    tablename = models.TextField()
    rulename = models.TextField()
    event = models.TextField()
    definition = models.TextField()

    class Meta:
        managed = False
