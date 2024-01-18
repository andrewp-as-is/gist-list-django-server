from django.apps import apps

from django_command_worker.models import Queue
from base.management.base import BaseCommand


MODEL_LIST = list(filter(
    lambda m:m._meta.db_table.endswith('_job'),
    apps.get_models()
))


class Command(BaseCommand):

    def handle(self,*args,**options):
        for model in MODEL_LIST:
            if model.objects.all().first():
                name = model._meta.db_table.replace('"','').replace('.','_')
                Queue.objects.get_or_create(name=name)
