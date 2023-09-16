__all__ = ['Following']

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class Following(models.Model):
    objects = Manager()

    user = models.ForeignKey('User', related_name='+',on_delete=models.CASCADE)
    following = models.ForeignKey('User', related_name='+',on_delete=models.CASCADE)

    class Meta:
        managed = False
        unique_together = ('user', 'following',)
