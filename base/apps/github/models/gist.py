__all__ = ["AbstractGist", "Gist"]

import re

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from base.apps.tag.utils import get_hashtag_list
from .language import Language


NAME2LANGUAGE = {l.name: l for l in Language.objects.all()}

"""
https://developer.github.com/v3/gists/
"""


class GistMixin:
    def display_name(self):  # todo?
        if "gistfile1." in self.filenames[0]:
            return "gist:%s" % self.id
        return self.filenames[0]


class AbstractGist(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    fork_of = models.ForeignKey("Gist", null=True, on_delete=models.DO_NOTHING)

    public = models.BooleanField(default=True)
    fork = models.BooleanField(default=False) # GraphQL api only

    description = models.CharField(max_length=256, null=True)
    filename_list = ArrayField(models.TextField())
    file_size_list = ArrayField(models.IntegerField())
    language_list = ArrayField(models.TextField())  # language name list
    raw_url_hash_list = ArrayField(models.TextField())

    version = models.TextField(null=True)

    size = models.IntegerField(default=0) # REST api only
    comments_count = models.IntegerField(default=0)
    forks_count = models.IntegerField(null=True) # GraphQL api only
    stargazers_count = models.IntegerField(null=True) # GraphQL api only
    revisions_count = models.IntegerField(null=True)

    created_at = models.IntegerField(null=True)
    pushed_at = models.IntegerField(null=True) # GraphQL api only
    updated_at = models.IntegerField(null=True)

    description_order = models.IntegerField(null=True)
    filename_order = models.IntegerField(null=True)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return "/%s/%s" % (
            self.owner.login,
            self.id,
        )

    def get_language_list(self):
        language_list = []
        for language_name in self.language_list or []:
            language = NAME2LANGUAGE.get(language_name, None)
            if language:
                language_list += [language]
        return language_list

    def get_tag_list(self):
        return list(
            map(lambda s: s.replace("#", ""), get_hashtag_list(self.description))
        )

    @property
    def filename2raw_url_hash(self):
        if len(self.filename_list or [])==len(self.raw_url_hash_list or []):
            return dict(map(lambda i,j:(i,j),self.filename_list,self.raw_url_hash_list))


class Gist(AbstractGist):
    id = models.CharField(max_length=100, primary_key=True)

    fork_of = models.ForeignKey("Gist", null=True, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(
        "github.User", related_name="+", on_delete=models.DO_NOTHING
    )

    class Meta:
        managed = False
