__all__ = ['PythonError',]

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class PythonError(models.Model):
    objects = Manager()

    filename = models.CharField(max_length=255)
    lineno = models.IntegerField()
    count = models.IntegerField(default=1)
    exc_type = models.CharField(max_length=255)
    exc_message = models.CharField(max_length=255)
    exc_traceback = models.TextField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-timestamp', )
        unique_together = [('filename','lineno',)]

    def get_absolute_url(self):
        return '/admin/error/pythonerror/%s/' % self.id
