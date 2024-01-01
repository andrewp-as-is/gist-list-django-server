__all__ = ['AbstractLanguage','Language']


from django.db import models

"""
https://raw.githubusercontent.com/ozh/github-colors/master/colors.json
"""

class AbstractLanguage(models.Model):
    name = models.TextField(unique=True)
    slug = models.TextField(unique=True)
    color = models.TextField(null=True)

    class Meta:
        abstract = True

class Language(AbstractLanguage):
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
