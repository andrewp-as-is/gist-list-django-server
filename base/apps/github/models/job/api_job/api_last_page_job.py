__all__ = ["ApiLastPageJob"]

from django.db import models


class ApiLastPageJob(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255,unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
