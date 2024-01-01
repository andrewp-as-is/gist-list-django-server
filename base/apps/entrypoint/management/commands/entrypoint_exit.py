from datetime import datetime
import os
import time

from django.core.management.base import BaseCommand

from ...models import Run

NAME = os.getenv('ENTRYPOINT_NAME')
TIMESTAMP = round(time.time(),3)

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("EXIT %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        Run.objects.filter(name=NAME).latest('id').update(finished_at=TIMESTAMP)
