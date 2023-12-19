__all__ = ['UserMeta',]

from django.db import models

class UserMeta(models.Model):
    user_id = models.IntegerField()

    refreshed_at = models.IntegerField()
    secret_refreshed_at = models.IntegerField()

    follower_modified_at = followers_count = models.IntegerField(null=True)
    following_modified_at = followers_count = models.IntegerField(null=True)
    gist_modified_at = followers_count = models.IntegerField(null=True)
    gist_language_modified_at = followers_count = models.IntegerField(null=True)
    gist_star_modified_at = followers_count = models.IntegerField(null=True)
    gist_tag_modified_at = followers_count = models.IntegerField(null=True)
    user_modified_at = followers_count = models.IntegerField(null=True)

    class Meta:
        managed = False
