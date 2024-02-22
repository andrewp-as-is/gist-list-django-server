__all__ = ["GistInsert", ]

from django.contrib.postgres.fields import ArrayField
from django.db import models

class GistInsert(models.Model):
    id = models.CharField(max_length=100,primary_key=True)

    fork_of = models.ForeignKey("Gist", null=True, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(
        "github.User", related_name="+", on_delete=models.DO_NOTHING
    )
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

    class Meta:
        managed = False
