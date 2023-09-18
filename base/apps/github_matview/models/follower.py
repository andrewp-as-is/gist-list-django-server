__all__ = ['AbstractFollower','Follower']

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class AbstractFollower(models.Model):
    objects = Manager()

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
