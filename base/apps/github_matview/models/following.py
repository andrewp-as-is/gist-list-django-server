__all__ = ['AbstractFollowing','Following']

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class AbstractFollowing(models.Model):
    objects = Manager()

    user = models.ForeignKey('User', related_name='+',on_delete=models.CASCADE)
    follower = models.ForeignKey('User', related_name='+',on_delete=models.CASCADE)

    login_order = models.IntegerField()
    name_order = models.IntegerField()
    followers_order = models.IntegerField()
    following_order = models.IntegerField()
    gists_order = models.IntegerField()

    class Meta:
        abstract = True

class Following(AbstractFollowing):
    class Meta:
        managed = False
        unique_together = ('user', 'follower',)
