
import os
from django.core.management.base import BaseCommand

from base.apps.github.models import Token, User

from base.apps.postgres.models import RelationSizeJob as Job
from django_bulk_create import bulk_create, execute_sql

SQL = """
INSERT INTO postgres.relation_size_capture(regclass,size)
SELECT format('"%s"."%s"',n.nspname,c.relname),
pg_total_relation_size(job.regclass)
FROM postgres_relation_size_job.job
JOIN pg_class AS c ON c.oid::regclass::text=job.regclass
JOIN pg_namespace AS n ON n.oid=c.relnamespace;
TRUNCATE postgres_relation_size_job.job;
"""

class Command(BaseCommand):

    def handle(self,*args,**options):
        print("TODO")
