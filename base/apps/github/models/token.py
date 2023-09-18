__all__ = ['Token',]

from datetime import datetime

from django.db import models

from base.utils import get_timestamp

"""
https://developer.github.com/v3/rate_limit/
"""


class Token(models.Model):
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.DO_NOTHING)
    token = models.TextField(unique=True)

    core_ratelimit_limit = models.IntegerField(null=True) # 5000/hour
    core_ratelimit_remaining = models.IntegerField(null=True)
    core_ratelimit_used = models.IntegerField(null=True)
    core_ratelimit_reset = models.IntegerField(null=True)

    graphql_ratelimit_limit = models.IntegerField(null=True) # 5000/hour
    graphql_ratelimit_remaining = models.IntegerField(null=True)
    graphql_ratelimit_used = models.IntegerField(null=True)
    graphql_ratelimit_reset = models.IntegerField(null=True)

    search_ratelimit_limit = models.IntegerField(null=True) # 30/hour
    search_ratelimit_remaining = models.IntegerField(null=True)
    search_ratelimit_used = models.IntegerField(null=True)
    search_ratelimit_reset = models.IntegerField(null=True)

    created_at = models.IntegerField(null=True)
    updated_at = models.IntegerField(null=True)

    class Meta:
        managed = False

    def update(self,headers):
        Token.objects.filter(id=self.id).update(
            rate_remaining=int(headers.get('X-RateLimit-Remaining')),
            rate_used=int(headers.get('X-RateLimit-Used')),
            reset_at=datetime.utcfromtimestamp(int(headers.get('X-RateLimit-Reset'))),
            updated_at=get_timestamp()
        )

"""
отзыв токена - revocation
отозван пользователем - revoked
"""
