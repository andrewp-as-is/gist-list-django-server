__all__ = ['JobDetect']

from django.db import models

class JobDetect(models.Model):
    schemaname = models.CharField(max_length=255)
    viewname = models.CharField(max_length=255)

    class Meta:
        managed = False

