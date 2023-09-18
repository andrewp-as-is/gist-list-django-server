__all__ = ['GistLanguage']

from django.db import models

class GistLanguage(models.Model):
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    language = models.ForeignKey('Language', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        unique_together = ('gist', 'language_id',)
