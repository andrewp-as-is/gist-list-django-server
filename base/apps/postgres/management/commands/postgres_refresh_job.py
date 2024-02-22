import time

from base.apps.postgres.models import Matview
from base.apps.job.management.base import JobCommand

"""
REFRESH MATERIALIZED VIEW "{schemaname}"."{matviewname}";
ALTER MATERIALIZED VIEW "{schemaname}"."{matviewname}" RENAME TO "{matviewname}.bak";
ALTER MATERIALIZED VIEW "{schemaname}"."{matviewname}.standby" RENAME TO "{matviewname}";
ALTER MATERIALIZED VIEW "{schemaname}"."{matviewname}.bak" RENAME TO "{matviewname}.standby";
"""

class Command(JobCommand):

    def do_job(self, job):
        #query = 'REFRESH MATERIALIZED VIEW "%s"."%s"' % (job.schemaname,job.matviewname)
        schemaname, matviewname = job.schemaname, job.matviewname
        query = """
REFRESH MATERIALIZED VIEW CONCURRENTLY "{schemaname}"."{matviewname}";
        """.format(schemaname=schemaname,matviewname=matviewname)
        self.execute_sql(query)
        defaults = {'refreshed_at':round(time.time(),3)}
        kwargs = {'schemaname':schemaname,'matviewname':matviewname}
        Matview.objects.update_or_create(defaults,**kwargs)
