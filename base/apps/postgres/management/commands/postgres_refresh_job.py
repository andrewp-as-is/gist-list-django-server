from django.core.management.base import BaseCommand

from base.utils import execute_sql

class Command(BaseCommand):

    def do_job(self, job):
        query = 'REFRESH MATERIALIZED VIEW "%s"."%s"' % (job.schemaname,job.matviewname)
        self.execute_sql(query)
