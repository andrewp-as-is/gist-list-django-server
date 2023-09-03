from datetime import date, datetime, timedelta
from django.template import Library
from django.utils.timesince import timesince


register = Library()

@register.filter
def gist_time(d):
    yesterday = date.today() - timedelta(days = 1)
    td = datetime.now() - d
    td_seconds = td.total_seconds()
    td_hours = int(td_seconds / (60*60))
    if td.days == 0 and td.total_seconds()<60:
        return 'now'
    if td.days == 0 and not td_hours:
        return '%s ago' % timesince(d).split(',')[0]
    if td.days == 0 and td.total_seconds()<60*60*2:
        return '1 hour ago'
    if td.days == 0  or (d.date() == yesterday and td_hours<=23):
        return '%s hours ago' % td_hours
    if d.date() == yesterday:
        return 'yesterday'
    if td.days<=31:
        return '%s days ago' % td.days
    return '%s ago' % timesince(d).split(',')[0]
    # return '%s at %s' % (d.strftime('%d %b').lower(),d.strftime('%H:%M'))

"""

@register.filter
def post_time(d):
    yesterday = date.today() - timedelta(days = 1)
    td = datetime.now() - d
    td_seconds = td.total_seconds()
    td_hours = int(td_seconds / (60*60))
    if td.days == 0 and td.total_seconds()<60:
        return 'just now'
    if td.days == 0 and not td_hours:
        return '%s ago' % timesince(d).split(',')[0]
    if td.days == 0 and td.total_seconds()<60*60*4:
        return '%s hours ago' % td_hours
    if d.date() == yesterday:
        return 'yesterday at %s' % d.strftime('%H:%M')
    return '%s at %s' % (d.strftime('%d %b').lower(),d.strftime('%H:%M'))
"""
