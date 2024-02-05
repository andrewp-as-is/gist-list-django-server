__all__ = ['AbstractUserFollowerInfoMatview','UserFollowerInfoMatview']

from django.db import models


class AbstractUserFollowerInfoMatview(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    follower = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True

class AbstractUserFollowerInfo(AbstractUserFollowerInfoMatview):
    class Meta:
        managed = False
        unique_together = ('user', 'follower',)
