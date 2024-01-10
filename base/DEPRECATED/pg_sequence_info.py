from django.apps import apps
from django.db import connection
from django.db import models
from management.base import BaseCommand

MODEL_ITERATOR = filter(
    lambda m: m._meta.db_table.endswith("_job") and m._meta.managed,
    apps.get_models(),
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        select_list = []
        for m in MODEL_ITERATOR:
            db_table = m._meta.db_table.replace('"', "")
            schemaname, tablename = db_table.split(".")
            select_list += [
                """
SELECT 42 AS id,'{schemaname}' AS schemaname,'{sequencename}' AS sequencename,last_value
FROM {schemaname}.{sequencename}""".format(
                    schemaname=schemaname, sequencename=tablename + "_id_seq"
                ).strip()
            ]
        sql = """
--DROP VIEW IF EXISTS public.pg_sequence_info;
CREATE OR REPLACE VIEW public.pg_sequence_info AS
%s""" % "\nUNION\n".join(
            select_list
        )
        cursor = connection.cursor()
        cursor.execute(sql.strip())
