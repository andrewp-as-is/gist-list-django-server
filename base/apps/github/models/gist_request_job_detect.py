__all__ = ['GistRequestJobDetect']

from django.db import models

class GistRequestJobDetect(models.Model):
    url = models.TextField()
    gist_id = models.IntegerField()

    class Meta:
        managed = False

