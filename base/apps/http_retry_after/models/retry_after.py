__all__ = ['RetryAfter']

from django.db import models

class RetryAfter(models.Model):
    domain = models.TextField(unique=True)
    retry_after = models.TextField()
    created_at = models.IntegerField()

    class Meta:
        managed = False

