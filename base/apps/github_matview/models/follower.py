__all__ = ['AbstractFollower','Follower']

from django.db import models


class AbstractFollower(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    follower = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    login_order = models.IntegerField()
    name_order = models.IntegerField()
    followers_order = models.IntegerField()
    following_order = models.IntegerField()
    gists_order = models.IntegerField()

    class Meta:
        abstract = True

class Follower(AbstractFollower):
    class Meta:
        managed = False
        unique_together = ('user', 'follower',)
