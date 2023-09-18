import os
import sys

from discord import SyncWebhook
from django.core.management.base import BaseCommand

from base.apps.incident.models import DiscordJob as Job, Incident
from base.apps.job.utils import save_cursor

URL = "https://discord.com/api/webhooks/1146811450787102741/6GTQLhrSiaWT2BY7tQi0nroCJrzbTWr6-W0WWXR9_v16atwtPMz4Uq7K9ZLe3yR48Z9P"

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
        webhook = SyncWebhook.from_url(URL)
        webhook.send(message)



