__all__ = ['Gist']

from django.db import models

from base.apps.github.models import AbstractGist

class Gist(AbstractGist):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('github.User',related_name='github_gist_new_matview_owner',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
