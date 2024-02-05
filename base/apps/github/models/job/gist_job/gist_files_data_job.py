__all__ = ["GistFilesDataJob"]

from django.db import models


class GistFilesDataJob(models.Model):
    id = models.AutoField(primary_key=True)
    gist_id = models.TextField(unique=True)
    data = models.TextField()

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
