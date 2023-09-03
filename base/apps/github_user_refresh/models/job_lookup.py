__all__ = ['JobLookup']

from django.db import models

class JobLookup(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
