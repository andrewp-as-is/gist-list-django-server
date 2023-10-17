__all__ = ['AbstractGist','Gist']

import re

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from base.apps.django_command.utils import create_job
from base.apps.tag.utils import get_hashtag_list
from .language import Language


NAME2LANGUAGE = {l.name:l for l in Language.objects.all()}

"""
https://developer.github.com/v3/gists/
"""

class GistMixin:

    def display_name(self): # todo?
        if 'gistfile1.' in self.filenames[0]:
            return 'gist:%s' % self.id
        return self.filenames[0]

class AbstractGist(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    fork_of = models.ForeignKey('Gist', null=True,on_delete=models.DO_NOTHING)

    public = models.BooleanField(default=True)
    fork = models.BooleanField(default=False)

    description = models.CharField(max_length=256, null=True)
    filename_list = ArrayField(models.TextField())
    language_list = ArrayField(models.TextField()) # language name list

    version = models.TextField(null=True)

    comments_count = models.IntegerField(default=0)
    files_count = models.IntegerField()
    forks_count = models.IntegerField(null=True)
    stargazers_count = models.IntegerField(null=True) # graphql only
    revisions_count = models.IntegerField(null=True)

    created_at = models.IntegerField(null=True)
    pushed_at = models.IntegerField(null=True)
    updated_at = models.IntegerField(null=True)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return '/%s/%s' % (self.owner.login,self.id,)

    def get_language_list(self):
        language_list = []
        for language_name in self.language_list or []:
            language = NAME2LANGUAGE.get(language_name,None)
            if language:
                language_list+=[language]
        return language_list

    def get_tag_list(self):
        return list(map(
            lambda s:s.replace('#',''),
            get_hashtag_list(self.description)
        ))

    def get_download_url(self):
        if self.version:
            return 'https://gist.github.com/%s/%s/archive/%s.zip' % (self.owner.login,self.id,self.version,)

class Gist(AbstractGist):
    id = models.CharField(max_length=100, primary_key=True)

    fork_of = models.ForeignKey('Gist', null=True,on_delete=models.DO_NOTHING)
    owner = models.ForeignKey('github.User',related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
