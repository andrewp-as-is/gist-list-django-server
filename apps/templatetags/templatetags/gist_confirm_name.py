from datetime import date, datetime, timedelta
from django.template import Library
from django.utils.timesince import timesince


register = Library()

@register.filter
def gist_confirm_name(gist):
    if gist.description_noemoji:
        return gist.description_noemoji.replace('"','').replace("'",'')
    return gist.files.split(',')[0].replace('"','').replace("'",'')
