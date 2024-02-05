__all__ = ['UserFollowingMatview']

from django.db import models
from .user_following import AbstractUserFollowing

class UserFollowingMatview(AbstractUserFollowing):
  # user = models.ForeignKey('User', related_name='user_following_matview_user',on_delete=models.DO_NOTHING)
  #  following = models.ForeignKey('User', related_name='user_following_matview_follower',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
