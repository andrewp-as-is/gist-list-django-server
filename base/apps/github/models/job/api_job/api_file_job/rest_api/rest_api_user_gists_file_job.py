__all__ = ["RestApiUserGistsFileJob"]

from django.db import models


class RestApiUserGistsFileJob(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    path = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    def response_match(self,response):
        return response.status==200 and '/user/' in response.request.url and '/gists' in response.request.url
