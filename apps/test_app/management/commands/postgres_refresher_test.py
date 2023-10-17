import time

from django.core.management.base import BaseCommand
from django.db.models import Count, Max, Min, Avg
from django_postgres_refresher.models import Report,Stat

class Command(BaseCommand):

    def handle(self,*args,**options):
        r_list = list(Report.objects.values('schemaname','matviewname').annotate(
            count=Count('duration'),
            avg_duration=Avg('duration'),
            min_duration=Min('duration'),
            max_duration=Max('duration')
        ))
        stat_list = list(Stat.objects.all())
        stat_create_list = []
        for r in row_list:
            stat_create_list+=[Stat(
                schemaname=r['schemaname'],
                matviewname=r['matviewname'],
                count=r['count'],
                avg_duration=round(r['avg_duration'],3),
                min_duration=round(r['min_duration'],3),
                max_duration=round(r['max_duration'],3)
            )]
        Stat.objects.bulk_create(stat_create_list,            update_conflicts=True,
            unique_fields = ['schemaname','matviewname'],
            update_fields = ['count','avg_duration','min_duration','max_duration']
        )
