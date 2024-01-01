from datetime import datetime
import os
import time

from django.core.management.base import BaseCommand

from ...models import Run

NAME = os.getenv('ENTRYPOINT_NAME')
TIMESTAMP = round(time.time(),3)

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("START %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        defaults = dict(started_at=TIMESTAMP)
        Run.objects.get_or_create(defaults,name=NAME)
