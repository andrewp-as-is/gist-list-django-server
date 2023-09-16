__all__ = ['Follower']

from django.db import models

from base.apps.github_matview.models import AbstractFollower

class Follower(AbstractFollower):
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.CASCADE)
    follower = models.ForeignKey('User', related_name='+',on_delete=models.CASCADE)

    class Meta:
        managed = False
        unique_together = [('user', 'follower',)]
