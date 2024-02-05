import time

from base.apps.postgres.models import Matview
from base.apps.job.management.base import JobCommand

class Command(JobCommand):

    def do_job(self, job):
        #query = 'REFRESH MATERIALIZED VIEW "%s"."%s"' % (job.schemaname,job.matviewname)
        schemaname, matviewname = job.schemaname, job.matviewname
        query = """
REFRESH MATVIEW "{schemaname}"."{matviewname}";
ALTER MATVIEW "{schemaname}"."{matviewname}" RENAME TO "{matviewname}.bak";
ALTER MATVIEW "{schemaname}"."{matviewname}.standby" RENAME TO "{matviewname}";
ALTER MATVIEW "{schemaname}"."{matviewname}.bak" RENAME TO "{matviewname}.standby";
        """.format(schemaname=schemaname,matviewname=matviewname)
        self.execute_sql(query)
        defaults = {'refreshed_at':round(time.time(),3)}
        kwargs = {'schemaname':schemaname,'matviewname':matviewname}
        Matview.objects.update_or_create(defaults,**kwargs)
