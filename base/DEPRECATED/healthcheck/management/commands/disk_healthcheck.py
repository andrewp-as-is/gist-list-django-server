import time
import psutil

from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.management.base import CheckCommand

MIN_SIZE = (2**30)*10 # 10 GB


class Command(CheckCommand):
    HEALTHCHECK_NAME = 'DISK'
    INCIDENT_NAME = 'DISK FULL'

    def check(self):
        disk = psutil.disk_usage('/')
        if disk.free<MIN_SIZE:
            raise CheckError('DISK FULL')
