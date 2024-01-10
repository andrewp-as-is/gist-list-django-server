__all__ = ['Follower']

from django.db import models

from base.apps.github_matview.models import AbstractFollower

class Follower(AbstractFollower):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.DO_NOTHING)
    follower = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        unique_together = [('user', 'follower',)]
