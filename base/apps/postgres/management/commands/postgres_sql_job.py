import logging
import time

from django.core.management.base import BaseCommand

from base.apps.postgres.models import SqlReport
from base.apps.postgres.models import SqlJob as Job
from django_bulk_create import bulk_create

class Command(BaseCommand):

    def handle(self,*args,**options):
        self.create_list = []
        job_list = list(Job.objects.all())
        for job in job_list:
            try:
                self.do_job(job)
            except Exception as e:
                # todo: postgres_error/database_error
                logging.error(e)
            finally:
                Job.objects.filter(id=job.id).delete()
        bulk_create(self.create_list)

    def do_job(self,job):
        started_at = time.time()
        execute_sql(job.sql)
        duration = time.time()-started_at
        self.create_list+=[SqlReport(
            sql = job.sql,
            duration=duration,
            timestamp=int(time.time())
        )]
