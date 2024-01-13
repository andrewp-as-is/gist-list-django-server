__all__ = ["GistStar"]

from django.db import models

from base.apps.github.models import AbstractGistStar


class GistStar(AbstractGistStar):

    class Meta:
        managed = False
        unique_together = (
            "gist",
            "user",
        )
