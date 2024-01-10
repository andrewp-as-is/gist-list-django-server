__all__ = ["RestApiUserGistsFileJob"]

from django.db import models


class RestApiUserGistsFileJob(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    path = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    @staticmethod
    def response_match(response):
        return response.status==200 and '/user/' in response.url and '/gists' in response.url
