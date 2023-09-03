__all__ = ['AbstractGist','Gist']

from django.db import models

from ...github.models import AbstractGist

class AbstractGist(AbstractGist):
    owner = models.ForeignKey('github.User',related_name='github_gist_matview_owner',on_delete=models.CASCADE)

    comments_order = models.IntegerField()
    stars_order = models.IntegerField()
    created_order = models.IntegerField()
    description_order = models.IntegerField()
    id_order = models.IntegerField()
    name_order = models.IntegerField()
    updated_order = models.IntegerField()

    class Meta:
        abstract = True

class Gist(AbstractGist):
    language_m2m = models.ManyToManyField('github.Language',through='GistLanguage',related_name='github_gist_matview_gist_languages')
    tag_m2m = models.ManyToManyField('tag.Tag',through='GistTag',related_name='github_gist_matview_gist_tags')

    class Meta:
        managed = False
