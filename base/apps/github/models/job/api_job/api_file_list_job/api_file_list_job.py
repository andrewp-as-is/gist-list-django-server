__all__ = ["ApiFileListJob"]

from django.db import models


class ApiFileListJob(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = True
