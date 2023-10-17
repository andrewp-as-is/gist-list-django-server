from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.management.base import CheckCommand
# from base.apps.http_request.models import Job
from base.apps.http_response.models import Response

class Command(CheckCommand):
    HEALTHCHECK_NAME = 'HTTP REQUEST'

    def check(self):
        qs = Response.objects.filter(timestamp__gt=int(time.time())-60)
        count = qs.count()
        if not count:
            raise CheckError('NOT WORKS')

