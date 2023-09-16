"""
job_table.table (schemaname,tablename,tuples)

schema_job.table_job:
1) schema_table_job.py              django command
2) CALL schema_job.table_job()      postgres procedure
"""

from django.core.management import get_commands
from django.core.management.base import BaseCommand

from base.apps.job_table.models import Procedure, Table
from base.apps.django_command_job.models import Job as DjangoCommandJob
from base.apps.postgres.models import SqlJob as PostgresSqlJob

from base.utils import bulk_create

REGPROC_LIST = list(map(
    lambda p:'"%s"."%s"' % (p.schemaname,p.proname),
    Procedure.objects.all()
))

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.create_list = []
        table_list = list(Table.objects.filter(tuples__gt=0))
        for table in table_list:
            command_name = '%s_%s' % (
                table.schemaname.replace('_job',''),
                table.tablename
            )
            # schema_table_job.py           Django command
            if command_name in get_commands():
                self.create_list+=[DjangoCommandJob(name=name)]
                continue
            # CALL schema_job.table_job()   PostgreSQL proc
            proname = '"%s"."%s"' % (table.schemaname,table.tablename)
            if proname in REGPROC_LIST:
                sql = 'CALL %s()' % proname
                self.create_list+=[PostgresSqlJob(sql=sql)]
                continue
            message_list = [
                "%s.%s command/procedure not found" % (table.schemaname,table.tablename),
                "%s.py django command not found" % command_name,
                "%s() postgres proc not found" % proname,
            ]
            raise ValueError("\n".join(message_list))
        bulk_create(self.create_list)
