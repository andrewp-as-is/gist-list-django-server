from base.apps.github.models import Token
from base.apps.healthcheck.exceptions import CheckError
from base.apps.healthcheck.management.base import CheckCommand
from base.apps.user.models import User

class Command(CheckCommand):
    HEALTHCHECK_NAME = 'GITHUB API TOKEN'
    INCIDENT_NAME = 'GITHUB API TOKEN'

    def check(self):
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            CheckError('SUPERUSER NOT FOUND')
        if not Token.objects.filter(user_id=admin.id).count():
            # token expired/invalid and was deleted
            CheckError('GITHUB TOKEN ISSUE')
