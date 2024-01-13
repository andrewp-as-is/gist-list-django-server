__all__ = ["RestApiUserGistsFileListJob"]

from django.contrib.postgres.fields import ArrayField
from django.db import models


class RestApiUserGistsFileListJob(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    path_list = ArrayField(models.TextField())

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = True
