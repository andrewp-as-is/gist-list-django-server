from datetime import datetime
import time
from urllib.parse import parse_qs, urlparse

from django.db import connection
from linkheader_parser import parse


def execute_sql(sql):
    cursor = connection.cursor()
    builtins.print(sql)
    timestamp = time.time()
    cursor.execute(sql)


def refresh_model_matview(model):
    db_table = model._meta.db_table.replace('"', "")
    schemaname = db_table.split(".")[0].replace('"', "")
    tablename = db_table.split(".")[1].replace('"', "")
    sql = 'REFRESH MATERIALIZED VIEW "%s"."%s"' % (schemaname, tablename)
    execute_sql(sql)
