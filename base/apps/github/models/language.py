from django.db import models

"""
https://raw.githubusercontent.com/ozh/github-colors/master/colors.json
"""

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['name'],
                update_fields = ['slug','color'],
            )
        return super().bulk_create(objs,**kwargs)


class Language(models.Model):
    objects = Manager()

    name = models.TextField(unique=True)
    slug = models.TextField(unique=True)
    color = models.TextField(null=True)

    class Meta:
        managed = False
