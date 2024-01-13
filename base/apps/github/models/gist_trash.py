__all__ = ['GistTrash']

from django.db import models

class GistTrash(models.Model):
    id = models.AutoField(primary_key=True)
    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
