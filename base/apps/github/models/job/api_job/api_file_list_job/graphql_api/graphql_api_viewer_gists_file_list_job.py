__all__ = ["GraphqlApiViewerGistsFileListJob"]

import re

from django.contrib.postgres.fields import ArrayField
from django.db import models


class GraphqlApiViewerGistsFileListJob(models.Model):
    user_id = models.IntegerField(unique=True)
    path_list = ArrayField(models.TextField())

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = True
