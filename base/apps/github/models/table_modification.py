__all__ = ["TableModification"]

from django.db import models


class TableModification(models.Model):
    user = models.OneToOneField(
        "github.User", related_name="+", on_delete=models.DO_NOTHING
    )
    follower_timestamp = models.IntegerField(null=True)
    following_timestamp = models.IntegerField(null=True)
    gist_timestamp = models.IntegerField(null=True)
    gist_language_timestamp = models.IntegerField(null=True)
    gist_tag_timestamp = models.IntegerField(null=True)
    user_timestamp = models.IntegerField(null=True)
    timestamp = models.IntegerField(null=True)

    class Meta:
        managed = False
