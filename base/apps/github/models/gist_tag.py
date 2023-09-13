__all__ = ['GistTag']

from django.db import models

from base.apps.django_command_job.utils import create_job

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        result = super().bulk_create(objs,**kwargs)
        create_job('github_gist_tag_after_insert')
        return result

class GistTag(models.Model):
    objects = Manager()

    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.CASCADE)
    tag = models.ForeignKey('tag.Tag', related_name='+',on_delete=models.CASCADE)

    class Meta:
        managed = False
        unique_together = [('gist', 'tag',)]
