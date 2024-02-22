__all__ = ['UserMapping']

from django.db import models

class UserMapping(models.Model):
    login = models.CharField(max_length=39,unique=True)
    user_id = models.IntegerField(null=True) # NULL = 404
    created_at = models.IntegerField()

    class Meta:
        managed = False
