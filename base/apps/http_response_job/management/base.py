import logging
import os
import sys

from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.template.defaultfilters import filesizeformat

from base.apps.error.utils import save_python_error
from base.apps.http_response.models import Response
from base.apps.http_response.utils import get_path
from base.apps.job_cursor.utils import save_cursor


"""
http_response.response
http_response_job.progress (regclass,response_id)
domain_xxx_response_job.job (response_id)
"""

class ResponseJobCommand(BaseCommand):
    JOB_CURSOR_NAME = None
    RESPONSE_JOB = None

    def handle(self, *args, **options):
        self.job_list = [] # prevent subclass errors
        self.response_list = [] # prevent subclass errors
        self.refresh_job_matview()
        self.id2response = {}
        self.response_id2job = {}
        self.job_list = list(self.RESPONSE_JOB.objects.all())
        if not self.job_list:
            self.response_list = []
            return print('SKIP: EMPTY')
        print('%s jobs' % len(self.job_list))
        self.response_list = list(Response.objects.filter(
            id__in=self.RESPONSE_JOB.objects.values_list('response_id',flat=True)
        ))
        if self.job_list:
            cursor_name = type(self).__module__.split('.')[-1] # name.py
            save_cursor(cursor_name,self.job_list)
        self.id2response = {r.id:r for r in self.response_list}
        self.response_id2job = {j.response_id:j for j in self.job_list}
        self.init()
        for job in self.job_list:
            try:
                self.do_job(job)
            except Exception as e:
                logging.error(e,exc_info=True)
                save_python_error(e)
                if settings.DEBUG:
                    raise e

    def init(self):
        pass

    def execute_sql(self,sql):
        cursor = connection.cursor()
        print(sql)
        cursor.execute(sql)

    def get_app_model_list(self):
        module_name = type(self).__module__
        app, name = module_name.split('.')[-4], module_name.split('.')[-1]
        return list(filter(
            lambda m:name in m._meta.db_table,
            apps.get_models()
        ))

    def do_job(self,job):
        response = self.get_response(job.response_id)
        if response:
            self.process_response(response)

    def get_response(self,response_id):
        return self.id2response[response_id]

    def process_response(self,response):
        method_name = 'process_%s_response' % response.status
        # пересоздавать автоматически опасно. возможно и не нужно
        print('%s status %s' % (response.url,response.status))
        if response.status==200:
            path = response.get_content_path()
            # self.message('%s path %s' % (response.url,path))
            if path:
                if not os.path.exists(path):
                    return print('%s\n%s NOT EXISTS' % (response.url,path))
                if not os.path.getsize(path):
                    return print('%s\n%s EMPTY' % (response.url,path))
                size = os.path.getsize(path)
                print('%s size %s' % (path,filesizeformat(size)))
        if hasattr(self,method_name):
            getattr(self,method_name)(response)
        else:
           print('%s NOT IMPLEMENTED' % method_name)

    def refresh_job_matview(self):
        db_table = self.RESPONSE_JOB._meta.db_table.replace('"','')
        sql = 'REFRESH MATERIALIZED VIEW "%s"."%s"' % (
            db_table.split('.')[0],
            db_table.split('.')[1]
        )
        self.execute_sql(sql)
