__all__ = ['Token','TokenBase']

from datetime import datetime

from django.db import models

"""
https://developer.github.com/v3/rate_limit/
"""


class Token(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('user.User', related_name='token',on_delete=models.DO_NOTHING)
    token = models.TextField(unique=True)

    core_ratelimit_limit = models.IntegerField(null=True) # 5000/hour
    core_ratelimit_remaining = models.IntegerField(null=True)
    core_ratelimit_used = models.IntegerField(null=True)
    core_ratelimit_reset_at = models.IntegerField(null=True)

    graphql_ratelimit_limit = models.IntegerField(null=True) # 5000/hour
    graphql_ratelimit_remaining = models.IntegerField(null=True)
    graphql_ratelimit_used = models.IntegerField(null=True)
    graphql_ratelimit_reset_at = models.IntegerField(null=True)

    search_ratelimit_limit = models.IntegerField(null=True) # 30/hour
    search_ratelimit_remaining = models.IntegerField(null=True)
    search_ratelimit_used = models.IntegerField(null=True)
    search_ratelimit_reset_at = models.IntegerField(null=True)

    created_at = models.IntegerField(null=True)
    updated_at = models.IntegerField(null=True)

    class Meta:
        managed = False


class TokenBase(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.TextField(unique=True)

    class Meta:
        managed = False

"""
отзыв токена - revocation
отозван пользователем - revoked
"""
