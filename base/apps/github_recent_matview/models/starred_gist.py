__all__ = ['StarredGist']

from django.db import models
from base.apps.github_default_matview.models import AbstractStarredGist


class StarredGist(AbstractStarredGist):
    owner = models.ForeignKey('github.User',related_name='github_recent_matview_starred_gist_owner',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
