__all__ = ["GistOrderJob"]

from django.db import models

class GistOrderJob(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
