import psutil

from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.management.base import CheckCommand


class Command(CheckCommand):
    HEALTHCHECK_NAME = 'CPU'
    INCIDENT_NAME = 'HIGH CPU USAGE'

    def check(self):
        percent = psutil.cpu_percent()
        if percent>80:
            raise CheckError('high cpu usage (%s%)' % percent)
