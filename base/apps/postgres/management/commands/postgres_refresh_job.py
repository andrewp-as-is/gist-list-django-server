import time

from base.apps.postgres.models import Matview
from management.base import JobCommand

class Command(JobCommand):

    def do_job(self, job):
        # todo: concurrently
        query = 'REFRESH MATERIALIZED VIEW "%s"."%s"' % (job.schemaname,job.matviewname)
        self.execute_sql(query)
        defaults = {'refreshed_at':round(time.time(),3)}
        kwargs = {'schemaname':job.schemaname,'matviewname':job.matviewname}
        Matview.objects.update_or_create(defaults,**kwargs)
