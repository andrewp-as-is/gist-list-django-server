__all__ = ["RestApiViewerGistsStarredFileJob"]

from django.db import models


class RestApiViewerGistsStarredFileJob(models.Model):
    user_id = models.IntegerField(unique=True)
    path = models.TextField()

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    def response_match(self,response):
        return response.status==200 and '/gists/starred?' in response.request.url
