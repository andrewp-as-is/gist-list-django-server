import time

from django.core.management.base import BaseCommand
from django.utils.timesince import timesince

from base.apps.django_command.models import Job as DjangoCommandJob
from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.models import Healthcheck
from base.apps.incident.models import Incident
from django_bulk_create import bulk_create


class CheckCommand(BaseCommand):
    HEALTHCHECK_NAME = None
    INCIDENT_NAME = None
    INCIDENT_INTERVAL = 3600

    def handle(self,*args,**options):
        self.create_list = []
        try:
            check = Healthcheck.objects.get(name=self.HEALTHCHECK_NAME)
        except Healthcheck.DoesNotExist:
            check = None
        success = True
        try:
            self.check()
        except Exception as e:
            if type(e)==CheckError:
                success = False
                incident_list =  Incident.objects.filter(
                    timestamp>int(time.time())-self.INCIDENT_INTERVAL
                )
                if not list(filter(lambda i:i.name==self.INCIDENT_NAME,incident_list)):
                    print(str(e))
                    self.create_list+=[Incident(
                        name=self.INCIDENT_NAME,
                        message=str(e),
                        timestamp=int(time.time())
                    )]
                    self.create_list+=[DjangoCommandJob(
                        name='incident_after_insert'
                    )]
        self.create_list+=[Healthcheck(
            name=self.HEALTHCHECK_NAME,
            success=success,
            timestamp=int(time.time())
        )]
        bulk_create(self.create_list)

    def check(self):
        raise NotImplementedError
