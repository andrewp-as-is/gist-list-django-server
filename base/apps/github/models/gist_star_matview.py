__all__ = ['GistStarMatview']

from django.db import models
from .gist_star import AbstractGistStar

class GistStarMatview(AbstractGistStar):
   # gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
   # user = models.ForeignKey('github.User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
