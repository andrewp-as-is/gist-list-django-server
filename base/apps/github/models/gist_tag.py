__all__ = ['GistTag']

from django.db import models


class GistTag(models.Model):
    id = models.IntegerField(primary_key=True)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    tag = models.ForeignKey('tag.Tag', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        unique_together = [('gist', 'tag',)]
