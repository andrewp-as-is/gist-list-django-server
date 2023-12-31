__all__ = ['Matview',]

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['schemaname','matviewname'],
                update_fields = ['timestamp']
            )
        result = super().bulk_create(objs,**kwargs)
        return result

class Matview(models.Model):
    objects = Manager()

    schemaname = models.TextField()
    matviewname = models.TextField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('schemaname','matviewname',)
        unique_together = [('schemaname','matviewname',)]

