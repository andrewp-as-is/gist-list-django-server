__all__ = ['GistTag']

from django.db import models

from base.utils import execute_sql

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        try:
            return super().bulk_create(objs,**kwargs)
        finally:
            execute_sql('VACUUM FULL github.gist_tag')

class GistTag(models.Model):
    objects = Manager()

    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.CASCADE)
    tag = models.ForeignKey('tag.Tag', related_name='+',on_delete=models.CASCADE)

    class Meta:
        managed = False
        unique_together = ('gist', 'tag',)
