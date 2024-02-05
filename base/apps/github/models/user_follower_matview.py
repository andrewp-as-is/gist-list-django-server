__all__ = ['UserFollowerMatview']

from django.db import models
from .user_follower import AbstractUserFollower

class UserFollowerMatview(AbstractUserFollower):
    user = models.ForeignKey('User', related_name='user_follower_matview_user',on_delete=models.DO_NOTHING)
    follower = models.ForeignKey('User', related_name='user_follower_matview_follower',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
