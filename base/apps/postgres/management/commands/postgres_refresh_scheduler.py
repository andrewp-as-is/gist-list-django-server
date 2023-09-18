import time

from django.core.management.base import BaseCommand

from base.utils import bulk_create, execute_sql
from ...models import Matview, RefreshReport, RefreshScheduler

SCHEDULER_LIST = list(RefreshScheduler.objects.all())

class Command(BaseCommand):

    def handle(self,*args,**options):
        create_list = []
        matview_list = list(Matview.objects.all())
        for scheduler in SCHEDULER_LIST:
            schemaname = scheduler.schemaname
            matviewname = scheduler.matviewname
            seconds = scheduler.seconds
            matview = next(filter(
                lambda m:m.schemaname==schemaname and m.matviewname==matviewname,
                matview_list
            ),None)
            if not matview or matview.timestamp+seconds<int(time.time()):
                # todo: CONCURRENTLY
                sql = 'REFRESH MATERIALIZED VIEW "%s"."%s";' % (schemaname,matviewname)
                timestamp = time.time()
                execute_sql(sql)
                create_list+=[Matview(
                    schemaname=schemaname,
                    matviewname=matviewname,
                    timestamp=int(timestamp)
                )]
                create_list+=[RefreshReport(
                    schemaname=schemaname,
                    matviewname=matviewname,
                    duration=time.time()-timestamp,
                    timestamp=int(timestamp)
                )]
        bulk_create(create_list)
