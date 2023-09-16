__all__ = ['UserProcedureJobDetect']

from django.db import models

class UserProcedureJobDetect(models.Model):
    regclass = models.TextField()
    user_id = models.IntegerField()

    class Meta:
        managed = False

