__all__ = ["UserFollowerRowNumberJob"]

from django.db import models

class UserFollowerRowNumberJob(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
