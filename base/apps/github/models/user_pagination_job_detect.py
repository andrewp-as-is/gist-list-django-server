__all__ = ['UserPaginationJobDetect']

from django.db import models

class UserPaginationJobDetect(models.Model):
    regclass = models.TextField()
    user_id = models.IntegerField()

    class Meta:
        managed = False

