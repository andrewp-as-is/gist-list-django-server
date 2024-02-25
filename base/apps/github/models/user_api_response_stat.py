__all__ = ['UserApiResponseStat',]

from django.db import models

class UserApiResponseStat(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    # REST API
    rest_api_profile_response_created_at = models.IntegerField(null=True)
    rest_api_public_gists_response_created_at = models.IntegerField(null=True)
    rest_api_authenticated_user_gists_response_created_at = models.IntegerField(null=True)
    rest_api_starred_gists_response_created_at = models.IntegerField(null=True)
    # GraphQL API
    graphql_api_followers_response_created_at = models.IntegerField(null=True)
    graphql_api_following_response_created_at = models.IntegerField(null=True)
    graphql_api_public_gists_response_created_at = models.IntegerField(null=True)
    graphql_api_authenticated_user_gists_response_created_at = models.IntegerField(null=True)

    class Meta:
        managed = False
