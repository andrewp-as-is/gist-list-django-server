__all__ = ["AbstractGist", "Gist"]

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField
from django.db import models

"""
https://developer.github.com/v3/gists/
"""


class GistMixin:
    def display_name(self):  # todo?
        if "gistfile1." in self.filenames[0]:
            return "gist:%s" % self.id
        return self.filenames[0]


class AbstractGist(models.Model):
    id = models.CharField(max_length=100,primary_key=False)

    public = models.BooleanField(default=True)

    description = models.CharField(max_length=256, null=True)
    filename_list = ArrayField(models.TextField())
    language_list = ArrayField(models.TextField())  # language name list
    tag_list = ArrayField(models.TextField())

    size = models.IntegerField(default=0) # REST api only
    comments_count = models.IntegerField(default=0)

    created_at = models.IntegerField(null=True)
    updated_at = models.IntegerField(null=True)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return "/%s/%s" % (
            self.owner.login,
            self.id,
        )


class Gist(AbstractGist):
    id = models.CharField(max_length=100,primary_key=True)

    fork_of = models.ForeignKey("Gist", null=True, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(
        "github.User", related_name="+", on_delete=models.DO_NOTHING
    )
    fork = models.BooleanField(default=False) # GraphQL api only

    forks_count = models.IntegerField(null=True) # GraphQL api only
    stargazers_count = models.IntegerField(null=True) # GraphQL api only

    created_at = models.IntegerField(null=True)
    pushed_at = models.IntegerField(null=True) # GraphQL api only

    version = models.TextField(null=True)
    revisions_count = models.IntegerField(null=True)

    row_number_over_id = models.IntegerField(null=True)
    row_number_over_comments = models.IntegerField(null=True)
    row_number_over_description = models.IntegerField(null=True)
    row_number_over_filename = models.IntegerField(null=True)
    row_number_over_forks = models.IntegerField(null=True)
    row_number_over_stargazers = models.IntegerField(null=True)
    row_number_over_created = models.IntegerField(null=True)
    row_number_over_updated = models.IntegerField(null=True)
    row_number_over_size = models.IntegerField(null=True)

    class Meta:
        managed = False
        unique_together = [('id', 'owner',)]
