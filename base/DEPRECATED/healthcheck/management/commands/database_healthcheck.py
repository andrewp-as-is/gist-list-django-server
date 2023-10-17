from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.management.base import CheckCommand

MAX_SIZE = (2**30)*10 # 10 GB


class Command(CheckCommand):
    HEALTHCHECK_NAME = 'DATABASE'
    INCIDENT_NAME = 'DATABASE FULL'

    def check(self):
        try:
            database_size = DatabaseSize.objects.all().first()
            if database_size and database_size.size>MAX_SIZE:
                raise CheckError('DISK FULL')
        except DatabaseSize.DoesNotExist:
            print('SKIP: not found')
