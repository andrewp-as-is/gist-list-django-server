import re
from django.template import Library


register = Library()

@register.filter
def gist_file_anchor(filename):
    return 'file-%s' % re.sub('-+', '-', re.sub("[^0-9a-z\-]+", "-", filename.lower()))
