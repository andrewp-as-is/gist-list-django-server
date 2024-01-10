__all__ = ["ApiGistsPublicRequestJob"]

from django.db import models


class ApiGistsPublicRequestJob(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.IntegerField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
