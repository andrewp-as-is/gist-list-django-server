__all__ = ['AbstractGistFile','GistFile']

from django.db import models


class AbstractGistFile(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    language = models.CharField(null=True,max_length=100)
    type = models.CharField(null=True,max_length=100)
    raw_url_hash = models.CharField(max_length=100)

    row_number_over_gist = models.IntegerField(null=True)
    row_number_over_name = models.IntegerField(null=True)
    row_number_over_size = models.IntegerField(null=True)
    row_number_over_type = models.IntegerField(null=True)

    class Meta:
        abstract = True

class GistFile(AbstractGistFile):
    class Meta:
        managed = False
        unique_together = [('gist', 'name',)]
