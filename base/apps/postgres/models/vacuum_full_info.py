__all__ = ['VacuumFullInfo']

from django.db import models

class VacuumFullInfo(models.Model):
    regclass = models.TextField() # DROP safe (regclass vs oid)
    duration = models.FloatField()
    size_before = models.TextField()
    size_after = models.TextField()
    timestamp = models.TextField()

    class Meta:
        managed = False

