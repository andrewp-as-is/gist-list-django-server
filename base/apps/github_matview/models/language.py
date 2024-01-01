from django.db import models

from base.apps.github.models import AbstractLanguage

class Language(AbstractLanguage):
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
