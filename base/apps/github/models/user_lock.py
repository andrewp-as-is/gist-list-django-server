__all__ = ['UserLock']

import time

from django.db import models

class UserLock(models.Model):
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    secret = models.BooleanField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('user', 'secret',)]

    def get_seconds(self):
        return int(time.time())-self.timestamp
