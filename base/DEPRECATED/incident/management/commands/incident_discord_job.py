import os
import sys

from discord import SyncWebhook
from django.core.management.base import BaseCommand

from base.apps.incident.models import DiscordJob as Job, Incident, DiscordWebhook
from base.apps.job.utils import save_cursor

DISCORD_WEBHOOK_LIST = list(DiscordWebhook.objects.all())

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.job_list = []
        try:
            self.job_list = list(Job.objects.all())
            for job in self.job_list:
                self.do_job(job)
        finally:
            if self.job_list:
                save_cursor(__name__.split('/')[-1],self.job_list[-1].id)

    def main(self):
        incident_list = list(Incident.objects.filter(
            id__in=Job.objects.values_list('incident_id',flat=True)
        ))
        self.id2incident = {i.id:i for i in incident_list}

    def do_job(self,job):
        incident = self.id2incident.get(job.incident_id,None)
        if not incident:
            return
        message = "incident#%s: %s\n%s" % (
            incident.id,
            incident.name,
            incident.message
        )
        for DISCORD_WEBHOOK_LIST in DISCORD_WEBHOOK_LIST:
            SyncWebhook.from_url(discord_webhook.url)
            webhook.send(message)



