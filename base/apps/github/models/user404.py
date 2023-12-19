__all__ = ['User404']

from django.db import models

class User404(models.Model):
    login = models.TextField(unique=True)
    created_at = models.IntegerField()

    class Meta:
        managed = False
