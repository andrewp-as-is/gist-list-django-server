__all__ = ['GistTsv']

from django.db import models

class GistTsv(models.Model):
    gist = models.ForeignKey('Gist', on_delete=models.DO_NOTHING)
    tsv = models.TextField()

    class Meta:
        managed = False
