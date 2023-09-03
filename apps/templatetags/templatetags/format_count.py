from django import template

from math import log, floor

register = template.Library()


@register.filter
def format_count(count):
    if count is None or count == "" or int(count) < 0:
        return ''
    count = int(count)
    if count == 0:
        return 0
    k = 1000.0
    units = ['', 'K', 'M', 'G', 'T', 'P']
    magnitude = int(floor(log(count, k)))
    format_string = '%.0f' if count > 100000 else '%.1f'
    value = format_string % (count / k**magnitude)
    return value.replace('.00', '').replace('.0', '') + units[magnitude]
