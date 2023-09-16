__all__ = ['GistLanguage']

from django.db import models

class GistLanguage(models.Model):
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.CASCADE)
    language_id = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('gist', 'language_id',)]
