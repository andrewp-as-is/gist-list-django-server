import time

from django.conf import settings

from base.management.base import BaseCommand
from ...models import Status, VacuumFull

RESTART_INTERVAL = getattr(settings, "WORKER_RESTART_INTERVAL", 600)
SLEEP_INTERVAL = getattr(settings, "WORKER_SLEEP_INTERVAL", 1)
RESTART_AT = int(time.time()) + RESTART_INTERVAL

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.execute_sql('VACUUM FULL status.status')
        while time.time() < RESTART_AT:
            kwargs = {'refreshed_at':round(time.time(),3)}
            vacuum_full = PostgresVacuumFull.objects.all().first()
            if vacuum_full and vacuum_full.duration>1:
                kwargs['postgres_vacuum_full'] = True
            Status.objects.update(**kwargs)
            time.sleep(SLEEP_INTERVAL)
