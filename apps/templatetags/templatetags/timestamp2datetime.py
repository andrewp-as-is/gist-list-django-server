from datetime import datetime as _datetime

from django.template import Library

register = Library()

@register.filter
def timestamp2datetime(timestamp):
    if timestamp:
        return _datetime.fromtimestamp(timestamp)
