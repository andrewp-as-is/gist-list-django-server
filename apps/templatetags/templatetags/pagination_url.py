from django import template
from django.utils.http import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def pagination_url(context, page):
    query = context['request'].GET.dict()
    query.update({'page':page})
    return urlencode(query)
