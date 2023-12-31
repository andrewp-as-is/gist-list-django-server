__all__ = ['StarredGist']

from django.db import models

from base.apps.github.models import AbstractGist

class StarredGist(AbstractGist):
    id = models.IntegerField(primary_key=True)
    stargazer = models.ForeignKey('User',related_name='github_gist_star_matview_stargazer',on_delete=models.DO_NOTHING)
    owner = models.ForeignKey('User',related_name='github_gist_star_matview_owner',on_delete=models.DO_NOTHING)

    starred_order = models.IntegerField()

    #language_m2m = models.ManyToManyField('Language',through='GistLanguage',related_name='github_matview_starred_gist_languages')
    #tag_m2m = models.ManyToManyField('tag.Tag',through='GistTag',related_name='github_matview_starred_gist_tags')

    class Meta:
        managed = False
