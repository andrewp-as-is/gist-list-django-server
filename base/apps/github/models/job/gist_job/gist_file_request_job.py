__all__ = ["GistFileRequestJob"]

from django.db import models


class GistFileRequestJob(models.Model):
    id = models.AutoField(primary_key=True)
    gist_id = models.TextField()
    filename = models.TextField()
    priority = models.IntegerField()

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
        unique_together = [('gist_id', 'filename',)]
