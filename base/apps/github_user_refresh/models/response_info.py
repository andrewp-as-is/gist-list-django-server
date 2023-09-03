__all__ = ['ResponseInfo']

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['user_id','url'],
                update_fields = ['etag','timestamp']
            )
        return super().bulk_create(objs,**kwargs)

class ResponseInfo(models.Model):
    objects = Manager()

    user = models.OneToOneField('github.User', related_name='+',on_delete=models.CASCADE)
    url = models.TextField()
    etag = models.TextField(null=True)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        unique_together = ('user', 'url',)
