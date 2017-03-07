from django import template
from apps.block.queries import BlockByUserDataView

register = template.Library()


@register.simple_tag()
def is_blocked(user, target):

    if BlockByUserDataView.is_blocked(target, user):
        return 'is-active'

    return ''


@register.inclusion_tag('block/_block_buttons.html')
def blocked(user, target):

    is_active = False
    if BlockByUserDataView.is_blocked(target, user):
        is_active = True

    return {
        'is_active': is_active,
        'target': target,
    }
