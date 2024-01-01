__all__ = ['GistStar']

from django.db import models

class GistStar(models.Model):
    id = models.IntegerField(primary_key=True)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.DO_NOTHING)
    order = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('gist', 'user',)]
