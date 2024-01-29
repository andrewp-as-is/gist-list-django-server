__all__ = ["GistFileContentRequestJob"]

from django.db import models


class GistFileContentRequestJob(models.Model):
    id = models.AutoField(primary_key=True)
    gist_id = models.TextField(unique=True)
    priority = models.IntegerField()

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
