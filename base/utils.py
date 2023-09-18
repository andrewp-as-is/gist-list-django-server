import builtins
from datetime import datetime, timezone
import os
import time

from django.conf import settings

from django.db import connection

from base.apps.django_command.models import Job as DjangoCommandJob
from base.apps.postgres.models import SqlJob, SqlReport

def bulk_create(obj_list,model2kwargs=None):
    model_list = list(set(map(lambda c:type(c),obj_list)))
    if not obj_list:
        return
    if not model2kwargs:
        model2kwargs = {}
    for model in sorted(model_list,key=lambda m:m._meta.db_table):
        _obj_list = list(filter(lambda c:isinstance(c,model),obj_list))
        db_table = model._meta.db_table.replace('"','')
        builtins.print('CREATE: %s %s' % (db_table,len(_obj_list)))
        # dict syntax: dict(Model={}) and {Model:{}}
        kwargs_list = [model2kwargs.get(k,None) for k in [model,model.__name__]]
        kwargs = next(filter(None,kwargs_list),None) or {}
        unique_fields = list(filter(
            lambda f:hasattr(f,'unique') and f.unique,
            model._meta.get_fields()
        ))
        model.objects.bulk_create(_obj_list,**kwargs)

def bulk_delete(obj_list):
    model_list = list(set(map(lambda d:type(d),obj_list)))
    for model in sorted(model_list,key=lambda m:m._meta.db_table):
        model_obj_list = list(filter(lambda d:isinstance(d,model),obj_list))
        id_list = list(map(lambda d:d.id,model_obj_list))
        db_table = model._meta.db_table.replace('"','')
        builtins.print('DELETE: %s %s' % (db_table,len(model_obj_list)))
        model.objects.filter(id__in=id_list).delete()
    create_list = []
    for model in model_list:
        db_table = model._meta.db_table.replace('"','')
        sql = 'VACUUM "%s"."%s";' % (db_table.split('.')[0],db_table.split('.')[1])
        create_list+=[SqlJob(sql=sql)]
    bulk_create(create_list)

def execute_sql(sql):
    cursor = connection.cursor()
    builtins.print(sql)
    timestamp = time.time()
    cursor.execute(sql)
    SqlReport(
        sql=sql,
        duration=time.time() - timestamp,
        timestamp = int(timestamp)
    ).save()

def iter_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

def print(msg):
    # todo: database?
    # if settings.DEBUG:
    tz = datetime.now(timezone.utc).astimezone().tzinfo
    dt = datetime.now().replace(tzinfo=tz).astimezone(tz=None)
    # todo: django already inited timezone
    builtins.print('[%s] %s' % (dt.strftime('%H:%M:%S'),msg))


def get_headers_text(data):
    return "\n".join(map(lambda i:'%s: %s' % (i[0],i[1]),data.items()))

def headers2str(data):
    if data:
        lines = []
        for k,v in data.items():
            lines.append('%s: %s' % (k,v))
        return "\n".join(sorted(lines))

def get_timestamp():
    return int(datetime.now().timestamp())

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
