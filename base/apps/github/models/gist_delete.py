__all__ = ['GistDelete']

from django.db import models

class GistDelete(models.Model):
    id = models.AutoField(primary_key=True)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
