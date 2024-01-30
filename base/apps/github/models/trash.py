__all__ = ['Trash']

from django.contrib.postgres.fields import ArrayField
from django.db import models

class Trash(models.Model):
    id = models.AutoField(primary_key=True)
    gist_id = models.TextField(unique=True)

    fork_of = models.ForeignKey("Gist", null=True, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(
        "github.User", related_name="+", on_delete=models.DO_NOTHING
    )
    public = models.BooleanField(default=True)

    description = models.CharField(max_length=256, null=True)
    filename_list = ArrayField(models.TextField())
    language_list = ArrayField(models.TextField())  # language name list

    deleted_at = models.IntegerField()

    class Meta:
        managed = False

    def get_absolute_url(self):
        return "/%s/trash/%s" % (
            self.owner.login,
            self.id,
        )
