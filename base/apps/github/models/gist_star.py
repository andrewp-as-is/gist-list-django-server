__all__ = ['GistStar']

from django.db import models

from base.utils import execute_sql


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['user_id','gist_id'],
                update_fields = ['order']
            )
        try:
            return super().bulk_create(objs,**kwargs)
        finally:
            execute_sql('VACUUM github.gist_star')

class GistStar(models.Model):
    objects = Manager()

    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.CASCADE)
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        managed = False
        unique_together = ('gist', 'user',)
