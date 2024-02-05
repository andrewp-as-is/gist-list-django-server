__all__ = ['AbstractStarredGistMatview','StarredGistMatview']

from django.db import models
from base.apps.github.models import AbstractGist


class AbstractStarredGistMatview(AbstractGist):
    id = models.AutoField(primary_key=True)
    stargazer_id = models.IntegerField()
    row_number_over_starred = models.IntegerField()

    class Meta:
        abstract = True

class StarredGistMatview(AbstractStarredGistMatview):
    owner = models.ForeignKey('github.User',related_name='github_default_matview_starred_gist_owner',on_delete=models.DO_NOTHING)
    owner = models.ForeignKey('github.User',related_name='github_default_matview_starred_gist_owner',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
