__all__ = ['GistTsv']

from django.db import models

class GistTsv(models.Model):
    id = models.IntegerField(primary_key=True)
    gist = models.ForeignKey('Gist', on_delete=models.DO_NOTHING)
    tsv = models.TextField()

    class Meta:
        managed = False
