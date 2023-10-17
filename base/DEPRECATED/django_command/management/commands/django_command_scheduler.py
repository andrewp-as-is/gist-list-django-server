import time

from django.core.management.base import BaseCommand

from django_bulk_create import bulk_create
from ...models import CallTime, Job, Scheduler

SCHEDULER_LIST = list(Scheduler.objects.all())

class Command(BaseCommand):

    def handle(self,*args,**options):
        create_list = []
        call_time_list = list(CallTime.objects.all())
        for scheduler in SCHEDULER_LIST:
            name = scheduler.name
            seconds = scheduler.seconds
            call_time = next(filter(
                lambda c:c.name==name,
                call_time_list
            ),None)
            if not call_time or call_time.timestamp+seconds<int(time.time()):
                create_list+=[Job(name=name)]
                create_list+=[CallTime(
                    name=name,timestamp=int(time.time()
                ))]
        bulk_create(create_list)
