__all__ = ['GistLanguage']

from django.db import models

class GistLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    language_id = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('gist', 'language_id',)]
