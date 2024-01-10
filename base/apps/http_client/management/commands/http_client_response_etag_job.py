from django.core.management.base import BaseCommand
from django.db import connection

SQL = 'CALL http_client.response_etag_job()'

class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute(SQL)
