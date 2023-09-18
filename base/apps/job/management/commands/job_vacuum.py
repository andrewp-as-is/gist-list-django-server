from django.core.management.base import BaseCommand

from base.apps.job.models import Table
from base.utils import execute_sql

class Command(BaseCommand):

    def handle(self, *args, **options):
        table_list = list(Table.objects.all())
        for t in table_list:
            sql = 'VACUUM "%s"."%s"' % (t.schemaname,t.tablename)
            execute_sql(sql)
