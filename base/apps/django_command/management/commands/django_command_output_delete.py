import os

from django.core.management.base import BaseCommand
from base.apps.django_command.conf import DJANGO_COMMAND_DIRNAME

"""
django_command/NAME/timestamp

TODO
delete report on delete files
by timestamp __lte=


"""

def delete_command_output_files(name):
    dirname = os.path.join(DJANGO_COMMAND_DIRNAME,name)
    if not os.path.exists(dirname):
        return
    name_list = list(os.listdir(dirname))
    for name in sorted(name_list)[1000:]:
        path = os.path.join(dirname,name)
        if os.path.exists(path):
            try:
                os.unlink(path)
            except Exception as e:
                logging.error(e)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not os.path.exists(DJANGO_COMMAND_DIRNAME):
            return print('SKIP: %s NOT EXISTS' % DJANGO_COMMAND_DIRNAME)
        for name in os.listdir(DJANGO_COMMAND_DIRNAME):
            delete_command_output_files(name)
