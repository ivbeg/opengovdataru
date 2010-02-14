from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('main_menu.html')
def main_menu(item, user=None):
    """Main top menu"""
    params = {}
    params['current_item'] = item
    params['menu_items'] = settings.SITE_MAIN_MENU
    if user is not None:
	params['user'] = user
    else:
	params['user'] = None
    return params
                        