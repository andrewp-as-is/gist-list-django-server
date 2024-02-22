from django.core.management.base import BaseCommand

from django.db import connection
from base.utils import execute_sql

SQL = """
select t.schemaname,t.relname
from pg_stat_all_tables AS t
join pg_class as c ON c.oid=t.relid
where c.relkind='r' AND t.schemaname!='pg_catalog' AND (t.n_dead_tup>0 OR t.n_live_tup!=c.reltuples);
""".strip()

class Command(BaseCommand):

    def handle(self,*args,**options):
        cursor = connection.cursor()
        cursor.execute(SQL)
        for r in cursor.fetchall():
            sql = 'VACUUM "%s"."%s"' % (r[0],r[1])
            print(sql)
            cursor.execute(sql)
