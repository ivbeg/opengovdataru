from django import template

register = template.Library()


@register.inclusion_tag('geticon.html')
def geticon(name):
    """Sidebar with help and vertical menu"""
    params = {}
    params['item'] = item
    return params
    