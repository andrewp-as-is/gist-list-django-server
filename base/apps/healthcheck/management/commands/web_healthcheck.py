import requests

from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.management.base import CheckCommand
from base.apps.healthcheck.models import Web

class Command(CheckCommand):
    HEALTHCHECK_NAME = 'WEB'
    INCIDENT_NAME = 'WEB CONTAINER'

    def check(self):
        self.incident_message = None
        for web in Web.objects.all():
            r = requests.get(web.url)
            if r.status_code not in [200]:
                raise CheckError('%s status %s' % (web.url,r.status_code))
