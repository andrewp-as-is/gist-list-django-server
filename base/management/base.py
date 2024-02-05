import collections
import os
import sys
import time

from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection

from django_command_worker.models import Queue
from base.apps.postgres.models import Query, RefreshJob
from django_stdout.management.base import StdoutMessageCommand

class BaseCommand(StdoutMessageCommand):
    MODEL2BULK_CREATE_KWARGS = {}

    def handle(self, *args, **options):
        self.delete_list = []
        self.model2create_list = collections.defaultdict(list)

    def init(self):
        self.job_command_name_list = []
        self.delete_list = []
        self.model2create_list = collections.defaultdict(list)

    def execute_sql(self, query):
        cursor = connection.cursor()
        self.stdout.write(query + "\n")
        created_at = time.time()
        cursor.execute(query)
        duration = round(time.time()-created_at,3)
        # todo: try except postgres.error
        Query(query=query,duration=duration,created_at=int(created_at)).save()

    def create(self,obj):
        self.model2create_list[type(obj)]+=[obj]

    def delete(self,obj):
        self.delete_list+=[obj]

    def create_job(self,job):
        command_name = type(job)._meta.db_table.replace('"','').replace('.','_')
        if command_name not in self.job_command_name_list:
            self.job_command_name_list+=[command_name]
            self.create(Queue(name=command_name))
            self.MODEL2BULK_CREATE_KWARGS[Queue] = dict(ignore_conflicts=True)

    def bulk_create(self):
        for model,obj_list in self.model2create_list.items():
            kwargs = self.MODEL2BULK_CREATE_KWARGS.get(model,{})
            schemaname,tablename = 'public', model._meta.db_table
            if '.' in model._meta.db_table:
                schemaname,tablename = model._meta.db_table.replace('"','').split('.')
            self.stdout.write('BULK CREATE: %s.%s: %s objects\n' % (schemaname,tablename,len(obj_list)))
            model.objects.bulk_create(obj_list,**kwargs)

    def bulk_delete(self):
        model2delete_list = collections.defaultdict(list)
        for obj in self.delete_list:
            model2delete_list[type(obj)]+=[obj]
        for model,obj_list in model2delete_list.items():
            schemaname,tablename = model._meta.db_table.replace('"','').split('.')
            self.stdout.write('BULK DELETE: %s.%s: %s objects\n' % (schemaname,tablename,len(obj_list)))
            id_list = list(map(lambda obj:obj.id,obj_list))
            model.objects.filter(id__in=id_list).delete()
