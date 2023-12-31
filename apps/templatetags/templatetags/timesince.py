from datetime import datetime, timedelta

from django.template import Library
from django.utils.timesince import timesince as _timesince

register = Library()

@register.filter
def timesince(d):
    if not d:
        return

    td = datetime.now() - d
    if td.days==0 and td.total_seconds()<60:
        return 'now'
    if td.days==0:
        return '%s ago' % _timesince(d).split(',')[0]
    if td.days<30:
        return '%s days ago' % td.days
    return d.strftime('%-d %b %Y')
