import os
import sys

from django.core.management.base import BaseCommand

from base.apps.error.models import PythonError

class Command(BaseCommand):
    def handle(self,*args,**options):
        return
        if sys.platform != "darwin":
            return
        error = PythonError.objects.latest('timestamp')
        if not error:
            return
        os.system("""
osascript -e 'display notification "{}" with title "{}"'
        """.format(error.exc_message, error.exc_type))
        os.system('/usr/bin/say python error &')
        if sys.stdout.isatty(): # Terminal
            os.system('tput bel')
