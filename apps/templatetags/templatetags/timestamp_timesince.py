from datetime import datetime, timedelta, timezone
import time

from django.template import Library
from utils import timesince

register = Library()

@register.filter
def timestamp_timesince(timestamp):
    if not timestamp:
        return
    return timesince(datetime.fromtimestamp(timestamp))
