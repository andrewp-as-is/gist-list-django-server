__all__ = ['GistRefresh']

from django.db import models

class GistRefresh(models.Model):
    id = models.AutoField(primary_key=True)
    gist = models.OneToOneField('github.Gist', related_name='+',on_delete=models.DO_NOTHING)
    started_at = models.FloatField()
    finished_at = models.FloatField(null=True)

    class Meta:
        managed = False

    def get_seconds(self):
        return self.finished_at - self.started_at
