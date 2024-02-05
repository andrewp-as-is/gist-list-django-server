__all__ = ['GistMatview']

from django.db import models
from .gist import AbstractGist

class GistMatview(AbstractGist):
    owner = models.ForeignKey('github.User',related_name='github_gist_matview_gist_owner',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
