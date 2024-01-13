__all__ = ['AbstractGistStar','GistStar']

from django.db import models


class AbstractGistStar(models.Model):
    id = models.AutoField(primary_key=True)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.DO_NOTHING)
    order = models.IntegerField()

    class Meta:
        abstract = True

class GistStar(AbstractGistStar):
    class Meta:
        managed = False
        unique_together = [('gist', 'user',)]
