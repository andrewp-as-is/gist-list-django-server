__all__ = ["GistStar"]

from django.db import models


class GistStar(models.Model):
    gist = models.ForeignKey("Gist", related_name="+", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        "github.User", related_name="+", on_delete=models.DO_NOTHING
    )
    starred_order = models.IntegerField()

    class Meta:
        managed = False
        unique_together = (
            "gist",
            "user",
        )
