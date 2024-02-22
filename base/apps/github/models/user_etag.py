__all__ = ['UserEtag']

from django.db import models

class UserEtag(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)

    profile_etag = models.CharField(max_length=255,null=True)
    gists_etag  = models.CharField(max_length=255,null=True)
    starred_gists_etag = models.CharField(max_length=255,null=True)
    graphql_gists_etag = models.CharField(max_length=255,null=True)
    graphql_followers_etag = models.CharField(max_length=255,null=True)
    graphql_following_etag = models.CharField(max_length=255,null=True)

    class Meta:
        managed = False
