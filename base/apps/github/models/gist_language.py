__all__ = ['GistLanguage']

from django.db import models

from base.utils import execute_sql

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        result = super().bulk_create(objs,**kwargs)
        execute_sql('VACUUM github.gist_language')
        return result

class GistLanguage(models.Model):
    objects = Manager()

    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.CASCADE)
    language_id = models.IntegerField()

    class Meta:
        managed = False
        unique_together = ('gist', 'language_id',)
