from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.management.base import CheckCommand
from base.apps.http_response.models import Response

class Command(CheckCommand):
    HEALTHCHECK_NAME = 'GITHUB API MAINTENANCE'
    INCIDENT_NAME = 'GITHUB API MAINTENANCE'

    def check(self):
        qs = Response.objects.filter(status__gte=500,timestamp__gt=int(time.time())-60)
        count = qs.count()
        if count:
            raise CheckError('Github API maintenance (5xx server error)')
