__all__ = ['GistResponseJobDetect']

from django.db import models

class GistResponseJobDetect(models.Model):
    viewname = models.TextField()
    gist_id = models.IntegerField()

    class Meta:
        managed = False

