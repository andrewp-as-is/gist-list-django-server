from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.management.base import CheckCommand
from base.apps.http_response.models import Response

class Command(CheckCommand):
    HEALTHCHECK_NAME = 'GITHUB API RATELIMIT'
    INCIDENT_NAME = 'GITHUB API RATELIMIT'

    def check(self):
        qs = Response.objects.filter(
            status=429,
            timestamp__gt=int(time.time())-60
        )
        count = qs.count()
        if count:
            raise CheckError('Github API ratelimit (Retry-After)')
