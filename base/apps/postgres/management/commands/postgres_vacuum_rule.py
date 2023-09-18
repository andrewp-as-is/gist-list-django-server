from django.core.management.base import BaseCommand

from base.utils import execute_sql
from ...models import Rule, Table

"""
INSERT with ON CONFLICT clause cannot be used with table that has INSERT or UPDATE rules
"""

class Command(BaseCommand):

    def handle(self, *args, **options):
        rule_list = list(Rule.objects.all())
        for t in Table.objects.exclude(tablename='sql_job'):
            table_rule_list = list(filter(
                lambda r:r.schemaname==t.schemaname and r.tablename==t.tablename,
                rule_list
            ))
            if t.tablename=='sql_job':
                continue
            sql = 'DROP RULE vacuum_on_update ON "%s"."%s";' % (t.schemaname,t.tablename)
            try:
                execute_sql(sql)
            except Exception:
                pass
            rule_name_list = list(map(lambda r:r.rulename,table_rule_list))
            if 'vacuum_on_delete' not in rule_name_list:
                sql = """
CREATE OR REPLACE RULE vacuum_on_delete AS ON DELETE to "{schema}"."{table}"
DO ALSO
INSERT INTO postgres.sql_job(sql)
SELECT format('VACUUM "{schema}"."{table}"')
ON CONFLICT(sql) DO NOTHING;
                """.format(schema=t.schemaname,table=t.tablename).strip()
                execute_sql(sql)
