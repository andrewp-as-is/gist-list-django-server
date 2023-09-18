import time

from django.core.management.base import BaseCommand

from base.utils import bulk_create
from ...models import Command as CommandModel, Job, Scheduler

SCHEDULER_LIST = list(Scheduler.objects.all())

class Command(BaseCommand):

    def handle(self,*args,**options):
        create_list = []
        command_list = list(CommandModel.objects.all())
        for scheduler in SCHEDULER_LIST:
            seconds = scheduler.seconds
            command = next(filter(
                lambda c:c.name==scheduler.name,
                command_list
            ),None)
            if not command or command.timestamp+seconds<int(time.time()):
                create_list+=[Job(name=scheduler.name)]
        bulk_create(create_list)
