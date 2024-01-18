"""
schema.name_job TABLE/VIEW
apps/schema/models.py class NameJob
apps/schema/management/commands/schema_name_job.py
"""

import logging
import os

from django.apps import apps
from django.conf import settings

from base.management.base import BaseCommand



class JobCommand(BaseCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.job_list = []  # prevent subclass errors
        self.job_model = self.get_job_model()
        qs = self.job_model.objects.order_by('id').select_related()
        self.job_list = list(qs)
        self.stdout.write('%s jobs\n' % len(self.job_list))
        if not self.job_list:
            return
        self.init()
        for job in self.job_list:
            try:
                self.do_job(job)
            except Exception as e:
                logging.error(e, exc_info=True)
                if settings.DEBUG:
                    raise e
        try:
            self.bulk_create()
            self.bulk_delete()
        except Exception as e:
            logging.error(e, exc_info=True)
            if settings.DEBUG:
                raise e
        max_id = max(list(map(lambda j: j.id, self.job_list)))
        self.job_model.objects.filter(id__lte=max_id).delete()

    def do_job(self,job):
        raise NotImplementedError

    def get_job_model(self):
        module_name = type(self).__module__
        app, name = module_name.split(".")[-4], module_name.split(".")[-1]
        for model in apps.get_models():
            if "." in model._meta.db_table:
                db_table = model._meta.db_table.replace('"', "")
                schemaname, relname = db_table.split(".")
                command = "%s_%s" % (schemaname, relname)
                if "%s_%s" % (schemaname, relname) == module_name.split(".")[-1]:
                    return model
        raise ValueError("Uknown job model for command %s" % name)
