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
    db_table = model._meta.db_table.replace('"','')
    schemaname = db_table.split('.')[0].replace('"','')
    tablename = db_table.split('.')[1].replace('"','')
    sql = 'REFRESH MATERIALIZED VIEW "%s"."%s"' % (schemaname,tablename)
    execute_sql(sql)


"""
   # for model in model_list:
    #    db_table = model._meta.db_table.replace('"','')
    #    sql = 'VACUUM "%s"."%s";' % (db_table.split('.')[0],db_table.split('.')[1])
    #    if next(filter(lambda c:type(c)==SqlJob and c.sql==sql,obj_list),None):
     #       obj_list+=[SqlJob(sql=sql)]
    for model in model_list:
        if model._meta.db_table.endswith('_job'):
            db_table = model._meta.db_table.replace('"','')
            name = db_table.replace('.','_')
            if next(filter(lambda c:type(c)==DjangoCommandJob and c.name==name,obj_list),None):
                obj_list+=[DjangoCommandJob(name=name)]
"""
