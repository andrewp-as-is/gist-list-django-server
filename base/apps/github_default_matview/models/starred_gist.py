__all__ = ['AbstractStarredGist','StarredGist']

from django.db import models
from base.apps.github.models import AbstractGist


class AbstractStarredGist(AbstractGist):
    id = models.AutoField(primary_key=True)
    starred_order = models.IntegerField()
    description_order = models.IntegerField()
    filename_order = models.IntegerField()
    forks_order = models.IntegerField()
    stars_order = models.IntegerField()
    updated_order = models.IntegerField()

    class Meta:
        abstract = True

class StarredGist(AbstractStarredGist):
    owner = models.ForeignKey('github.User',related_name='github_default_matview_starred_gist_owner',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
