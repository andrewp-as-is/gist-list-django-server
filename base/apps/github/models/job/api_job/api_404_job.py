__all__ = ["Api404Job"]

from django.db import models


class Api404Job(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField()

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    def response_match(self,response):
        return response.status==404
