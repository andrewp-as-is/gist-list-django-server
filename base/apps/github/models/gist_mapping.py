__all__ = ['GistOwner']

from django.db import models

class GistOwner(models.Model):
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    owner = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
