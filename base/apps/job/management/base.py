from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection


"""
schema.name_job TABLE/VIEW
schema.name_job_snapshot MATVIEW (static copy)
apps/schema/models.py class NameJob,class NameJobSnapshot
apps/schema/management/commands/schema_name_job.py
"""

class JobCommand(BaseCommand):

    def init(self):
        pass

    def execute_sql(self,sql):
        cursor = connection.cursor()
        print(sql)
        cursor.execute(sql)

    def get_job_model(self):
        module_name = type(self).__module__
        app, name = module_name.split('.')[-4], module_name.split('.')[-1]
        for model in apps.get_models():
            if '.' in model._meta.db_table:
                db_table = model._meta.db_table.replace('"','')
                schemaname, relname = db_table.split('.')
                #print('schemaname, relname: %s' % (schemaname, relname))
                command = '%s_%s' % (schemaname, relname)
                #print('command: %s' % command)
                if '%s_%s' % (schemaname, relname) == module_name.split('.')[-1]:
                    return model
        raise ValueError('Uknown job model for command %s' % name)

    def get_job_snapshot_model(self):
        module_name = type(self).__module__
        job_model = self.get_job_model()
        db_table = job_model._meta.db_table+'_snapshot'
        for model in apps.get_models():
            if model._meta.db_table==db_table:
                return model

    def refresh_snapshot(self):
        snapshot_model = self.get_job_snapshot_model()
        if snapshot_model:
            db_table = snapshot_model._meta.db_table.replace('"','')
            sql = 'REFRESH MATERIALIZED VIEW "%s"."%s"' % (
                db_table.split('.')[0],
                db_table.split('.')[1]
            )
            self.execute_sql(sql)
        # todo: matview.timestamp, matview report

    def truncate(self):
        # TRUNCATE schema.name_job
        db_table = self.get_job_model()._meta.db_table.replace('"','')
        sql = 'TRUNCATE "%s"."%s"' % (
            db_table.split('.')[0],
            db_table.split('.')[1]
        )
        self.execute_sql(sql)
