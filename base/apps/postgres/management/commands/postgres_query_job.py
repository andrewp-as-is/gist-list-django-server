import time

from base.apps.postgres.models import Query
from management.base import JobCommand

class Command(JobCommand):

    def do_job(self, job):
        created_at = round(time.time(),3)
        self.execute_sql(job.query)
        duration = round(time.time()-created_at,3)
        Query(query=job.query,created_at=created_at,duration=duration)
