import logging
import os
import sys

from django.apps import apps
from django.conf import settings
from django.db import connection
from django.template.defaultfilters import filesizeformat

from base.apps.error.utils import save_python_error
from base.apps.http_response.models import Response
from base.apps.http_response.utils import get_path
from base.apps.job.utils import save_cursor
from base.apps.job.management.base import JobCommand

"""
http_response.response
domain_job.xxx_response_job (response_id,object_id)
"""

class ResponseJobCommand(JobCommand):
    def handle(self, *args, **options):
        self.job_list = [] # prevent subclass errors
        self.response_list = [] # prevent subclass errors
        self.id2response = {}
        self.response_id2job = {}
        Job = self.get_job_model()
        self.refresh_snapshot() # schema.name_job_snapshot MATVIEW
        self.job_list = list(Job.objects.all())
        if not self.job_list:
            return
        print('%s jobs' % len(self.job_list))
        self.response_list = list(Response.objects.filter(
            id__in=Job.objects.values_list('response_id',flat=True)
        ))
        if self.job_list:
            save_cursor(Job,self.job_list[-1].id)
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
