__all__ = ['UserGistOrder']

from django.db import models

class UserGistOrder(models.Model):

    gist = models.OneToOneField('github.Gist', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
