__all__ = ['Gist']

from django.db import models

from ...github.models import AbstractGist

class Gist(AbstractGist):
    stargazer = models.ForeignKey('github.User',related_name='github_gist_star_new_matview_stargazer',on_delete=models.CASCADE)
    owner = models.ForeignKey('github.User',related_name='github_gist_star_new_matview_owner',on_delete=models.CASCADE)

    starred_order = models.IntegerField()

    language_m2m = models.ManyToManyField('github.Language',through='GistLanguage',related_name='github_gist_star_new_matview_gist_languages')
    tag_m2m = models.ManyToManyField('tag.Tag',through='GistTag',related_name='github_gist_star_new_matview_gist_tags')

    class Meta:
        managed = False
