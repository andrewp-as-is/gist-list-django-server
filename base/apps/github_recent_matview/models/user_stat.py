__all__ = ['UserStat']

from django.db import models

from base.apps.github.models import AbstractUserStat

class UserStat(AbstractUserStat):

    class Meta:
        managed = False
