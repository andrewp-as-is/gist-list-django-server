__all__ = ['AbstractGist','Gist']

import re

from django.db import models
from base.apps.github.models import AbstractGist


class AbstractGist(AbstractGist):
    id = models.AutoField(primary_key=True)
    id_order = models.IntegerField()
    description_order = models.IntegerField()
    filename_order = models.IntegerField()
    comments_order = models.IntegerField()
    forks_order = models.IntegerField()
    stars_order = models.IntegerField()
    created_order = models.IntegerField()
    updated_order = models.IntegerField()

    class Meta:
        abstract = True

class Gist(AbstractGist):
    owner = models.ForeignKey('github.User',related_name='github_matview_gist_owner',on_delete=models.DO_NOTHING)

    #language_m2m = models.ManyToManyField('Language',through='GistLanguage',related_name='github_matview_gist_languages')
    #tag_m2m = models.ManyToManyField('tag.Tag',through='GistTag',related_name='github_matview_gist_tags')


    class Meta:
        managed = False
