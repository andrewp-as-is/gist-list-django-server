from django.db import models

from base.apps.github.models import AbstractLanguage

class Language(AbstractLanguage):
    class Meta:
        managed = False
