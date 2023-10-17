from django.core.management import call_command, get_commands
from django.core.management.base import BaseCommand



class Command(BaseCommand):

    def handle(self,*args,**options):
        for name in get_commands().keys():
            if '_healthcheck' in name:
                call_command(name)
