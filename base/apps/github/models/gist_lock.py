__all__ = ['GistLock']

import time

from django.db import models

class GistLock(models.Model):
    id = models.IntegerField(primary_key=True)
    gist = models.OneToOneField('github.Gist', related_name='+',on_delete=models.DO_NOTHING)
    created_at = models.IntegerField()

    class Meta:
        managed = False

    def get_seconds(self):
        return int(time.time())-self.timestamp
