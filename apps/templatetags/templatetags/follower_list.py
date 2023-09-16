from django import template
register = template.Library()

@register.simple_tag
def follower_list(follower_list):
    return list(map(lambda f:f.follower,follower_list))
