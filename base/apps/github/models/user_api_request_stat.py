__all__ = ['UserApiRequestStat']

from django.db import models

class UserApiRequestStat(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    # REST API
    rest_api_profile_request_created_at = models.IntegerField(null=True)
    rest_api_public_gists_request_created_at = models.IntegerField(null=True)
    rest_api_authenticated_user_gists_request_created_at = models.IntegerField(null=True)
    rest_api_starred_gists_request_created_at = models.IntegerField(null=True)
    # GraphQL API
    graphql_api_followers_request_created_at = models.IntegerField(null=True)
    graphql_api_following_request_created_at = models.IntegerField(null=True)
    graphql_api_public_gists_request_created_at = models.IntegerField(null=True)
    graphql_api_authenticated_user_gists_request_created_at = models.IntegerField(null=True)

    class Meta:
        managed = False
