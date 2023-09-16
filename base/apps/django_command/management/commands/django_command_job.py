"""
django_command.config (name,output)
django_command.job (id,name,priority)
django_command.output (name,timestamp)
django_command.info (id,name,...)
"""

import io
import logging
import os
import sys
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

from base.apps.django_command.utils import get_output_path
from base.apps.error.utils import save_python_error
from base.utils import bulk_create, execute_sql
from ...models import CallReport, Command as _Command, Config, Job, Output

NAME2CONFIG = {c.name:c for c in Config.objects.all()}

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.create_list = []
        execute_sql('CALL django_command.insert()')
        job_list = list(Job.objects.exclude(
            name='django_command_job' # prevent endless loop
        ).order_by('-priority'))
        self.command_list = list(_Command.objects.all())
        for job in job_list:
            self.process_job(job)
        bulk_create(self.create_list)

    def process_job(self,job):
        config = NAME2CONFIG.get(job.name,'')
        timestamp = time.time()
        if settings.DEBUG:
            print('CALL COMMAND: %s' % job.name)
        old_stdout = sys.stdout
        sys.stdout = new_stdout = io.StringIO()
        try:
            call_command(job.name)
        except Exception as e:
            logging.error(e)
            save_python_error(e)
            if settings.DEBUG:
                sys.exit(1)
        finally:
            duration = time.time() - timestamp
            Job.objects.filter(id=job.id).delete() # prevent endless loop
            sys.stdout = old_stdout
            output = new_stdout.getvalue()
            if output:
                if settings.DEBUG:
                    print(output)
                if config and config.output:
                    self.create_list+=[Output(
                        name=job.name,timestamp=int(timestamp)
                    )]
                    path = get_output_path(job.name,int(timestamp))
                    dirname = os.path.dirname(path)
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                    open(path,'w').write(output)
            self.create_list+=[CallReport(
                name=job.name,duration=duration,timestamp=int(timestamp)
            )]
            self.create_list+=[_Command(
                name=job.name,duration=duration,timestamp=int(timestamp)
            )]
