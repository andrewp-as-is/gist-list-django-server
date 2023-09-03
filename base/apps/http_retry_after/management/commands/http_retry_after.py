import time

from django.core.management.base import BaseCommand

from apps.http_retry_after.models import RetryAfter

"""
Retry-After: 15
"""

class Command(BaseCommand):
    def handle(self, *args, **options):
        delete_ids = []
        for r in RetryAfter.objects.all():
            value = r.retry_after.split(':')[1].strip()
            if value.isdigit() and int(value)+seconds<int(time.time()):
                delete_ids+=[r.id]
        RetryAfter.objects.filter(id__in=delete_ids).delete()
