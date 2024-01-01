__all__ = ["RestApiUserProfileFileJob"]

from django.db import models


class RestApiUserProfileFileJob(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    def response_match(self,response):
        return response.status==200 and '/user/' in response.request.url and response.request.url.split('/')[-1].isdigit()
