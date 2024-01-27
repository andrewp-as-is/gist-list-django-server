__all__ = ['GistFileBackup']

from django.db import models


class GistFileBackup(models.Model):
    id = models.AutoField(primary_key=True)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    filename = models.TextField()
    created_at = models.IntegerField()

    class Meta:
        abstract = True
