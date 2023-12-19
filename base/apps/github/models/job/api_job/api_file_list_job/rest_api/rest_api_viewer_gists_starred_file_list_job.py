__all__ = ["ApiViewerGistsStarredFileListJob"]

import re

from django.contrib.postgres.fields import ArrayField
from django.db import models


class ApiViewerGistsStarredFileListJob(models.Model):
    user_id = models.IntegerField(unique=True)
    path_list = ArrayField(models.TextField())

    URL_REGEX = re.compile('https://api.github.com/gists/starred?+')

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = True
