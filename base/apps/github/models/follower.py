__all__ = ['Follower']

from django.db import models

class Follower(models.Model):
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    follower = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        unique_together = ('user', 'follower',)
