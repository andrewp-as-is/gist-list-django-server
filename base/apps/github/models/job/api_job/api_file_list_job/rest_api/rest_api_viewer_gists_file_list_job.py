__all__ = ["ApiViewerGistsFileListJob"]

import re

from django.contrib.postgres.fields import ArrayField
from django.db import models


class ApiViewerGistsFileListJob(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    path_list = ArrayField(models.TextField())

    URL_REGEX = re.compile('https://api.github.com/gists?+')

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = True
