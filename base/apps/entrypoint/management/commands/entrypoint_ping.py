"""
entrypoint.sh

export ENTRYPOINT_NAME="NAME"

python3 -u manage.py entrypoint_ping
...
python3 -u manage.py entrypoint_ping
"""

from datetime import datetime
import os
import time

from django.core.management.base import BaseCommand

from ...models import Ping

NAME = os.getenv('ENTRYPOINT_NAME')

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("ENTRYPOING PING %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        Ping(name=NAME,created_at=int(time.time())).save()
