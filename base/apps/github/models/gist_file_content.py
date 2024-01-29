__all__ = ['GistFileContent']

from django.db import models


class GistFileContent(models.Model):
    id = models.AutoField(primary_key=True)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    filename = models.TextField()
    raw_url_hash = models.TextField() # https://gist.githubusercontent.com/USER/GIST/raw/HASH/FILENAME

    class Meta:
        abstract = True
        unique_together = [('gist', 'filename',)]
