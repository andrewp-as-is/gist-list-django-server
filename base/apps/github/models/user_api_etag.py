__all__ = ['UserApiEtag']

from django.db import models

class UserApiEtag(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)

    # REST API
    rest_api_profile_etag = models.CharField(max_length=255,null=True)
    rest_api_public_gists_etag = models.CharField(max_length=255,null=True)
    rest_api_authenticated_user_gists_etag = models.CharField(max_length=255,null=True)
    rest_api_starred_gists_etag = models.CharField(max_length=255,null=True)
    # GraphQL API
    graphql_api_followers_etag = models.CharField(max_length=255,null=True)
    graphql_api_following_etag = models.CharField(max_length=255,null=True)
    graphql_api_public_gists_etag = models.CharField(max_length=255,null=True)
    graphql_api_authenticated_user_gists_etag = models.CharField(max_length=255,null=True)

    class Meta:
        managed = False

