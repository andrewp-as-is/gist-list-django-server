__all__ = ["GistTagJob"]

from django.db import models

class GistTagJob(models.Model):
    id = models.AutoField(primary_key=True)
    gist_id = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
