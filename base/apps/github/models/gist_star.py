__all__ = ['AbstractGistStar','GistStar']

from django.db import models


class AbstractGistStar(models.Model):
    id = models.AutoField(primary_key=True)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.DO_NOTHING)

    row_number_over_starred = models.IntegerField()
    row_number_over_description = models.IntegerField(null=True)
    row_number_over_filename = models.IntegerField(null=True)
    row_number_over_forks = models.IntegerField(null=True)
    row_number_over_stargazers = models.IntegerField(null=True)

    class Meta:
        abstract = True

class GistStar(AbstractGistStar):
    class Meta:
        managed = False
        unique_together = [('gist', 'user',)]
