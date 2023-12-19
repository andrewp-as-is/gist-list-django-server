__all__ = ["RestApiUserFollowersFileJob"]

from django.db import models


class RestApiUserFollowersFileJob(models.Model):
    user_id = models.IntegerField()
    path = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    def response_match(self,response):
        return response.status==200 and '/user/' in response.request.url and '/followers' in response.request.url
