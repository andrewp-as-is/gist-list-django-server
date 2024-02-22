__all__ = ["ApiGraphqlFollowersRequestJob"]

from django.db import models

class ApiGraphqlFollowersRequestJob(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    priority = models.IntegerField()

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
