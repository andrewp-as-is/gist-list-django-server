__all__ = ['GistLanguage']

from django.db import models

class GistLanguage(models.Model):
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.CASCADE)
    language = models.ForeignKey('github.Language', related_name='+',on_delete=models.CASCADE)

    class Meta:
        managed = False
        unique_together = ('gist', 'language',)
