import psutil

from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.management.base import CheckCommand


class Command(CheckCommand):
    HEALTHCHECK_NAME = 'MEMORY'
    INCIDENT_NAME = 'HIGH MEMORY USAGE'

    def check(self):
        percent = psutil.virtual_memory().percent
        if percent>90:
            raise CheckError('high memory usage (%ss)' % percent)
