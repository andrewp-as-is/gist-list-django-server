__all__ = ["UserTagJob"]

from django.db import models

class UserTagJob(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
