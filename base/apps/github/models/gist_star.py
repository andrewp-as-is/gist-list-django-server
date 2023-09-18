__all__ = ['GistStar']

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['user_id','gist_id'],
                update_fields = ['order']
            )
        result = super().bulk_create(objs,**kwargs)
        return result

class GistStar(models.Model):
    objects = Manager()

    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.DO_NOTHING)
    order = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('gist', 'user',)]
