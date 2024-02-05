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
    id = models.CharField(max_length=100, primary_key=True)

    fork_of = models.ForeignKey("Gist", null=True, on_delete=models.DO_NOTHING)

    public = models.BooleanField(default=True)
    fork = models.BooleanField(default=False) # GraphQL api only

    description = models.CharField(max_length=256, null=True)
    filename_list = ArrayField(models.TextField())
    size_list = ArrayField(models.IntegerField())
    raw_url_hash_list = ArrayField(models.TextField())
    language_list = ArrayField(models.TextField())  # language name list
    tag_list = ArrayField(models.TextField())

    version = models.TextField(null=True)

    size = models.IntegerField(default=0) # REST api only
    comments_count = models.IntegerField(default=0)
    forks_count = models.IntegerField(null=True) # GraphQL api only
    stargazers_count = models.IntegerField(null=True) # GraphQL api only
    revisions_count = models.IntegerField(null=True)

    created_at = models.IntegerField(null=True)
    pushed_at = models.IntegerField(null=True) # GraphQL api only
    updated_at = models.IntegerField(null=True)

    row_number_over_comments = models.IntegerField(null=True)
    row_number_over_description = models.IntegerField(null=True)
    row_number_over_filename = models.IntegerField(null=True)
    row_number_over_forks = models.IntegerField(null=True)
    row_number_over_stargazers = models.IntegerField(null=True)
    # row_number_over_id = id
    # row_number_over_created = created_at,id
    # row_number_over_updated = updated_at,id
    # row_number_over_sizes = size,id

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return "/%s/%s" % (
            self.owner.login,
            self.id,
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
