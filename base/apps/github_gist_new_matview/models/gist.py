__all__ = ['Gist']

from django.db import models

from ...github_gist_matview.models import AbstractGist

class Gist(AbstractGist):
    owner = models.ForeignKey('github.User',related_name='github_gist_new_matview_owner',on_delete=models.CASCADE)

    language_m2m = models.ManyToManyField('github.Language',through='GistLanguage',related_name='github_gist_new_matview_gist_languages')
    tag_m2m = models.ManyToManyField('tag.Tag',through='GistTag',related_name='github_gist_new_matview_gist_tags')


    class Meta:
        managed = False
