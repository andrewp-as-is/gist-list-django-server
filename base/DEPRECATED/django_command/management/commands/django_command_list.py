from django.core.management import get_commands
from django.core.management.base import BaseCommand

from django_bulk_create import bulk_create
from django_bulk_delete import bulk_delete
from ...models import Command as _Command

class Command(BaseCommand):

    def handle(self,*args,**options):
        create_list = []
        delete_list = []
        name2app = dict(get_commands().items())
        command_list = list(_Command.objects.all())
        name_list = list(map(lambda c:c.name,command_list))
        for command in command_list:
            if command.name not in name2app:
                delete_list+=[command]
        for name,app in name2app.items():
            if name not in name_list:
                create_list+=[_Command(
                    name=name,app=app
                )]
        bulk_create(create_list)
        bulk_delete(delete_list)
