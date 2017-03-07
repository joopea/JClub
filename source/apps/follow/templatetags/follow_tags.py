from django import template
from apps.follow.queries import FollowUserDataView

register = template.Library()


@register.inclusion_tag('follow/_follow_buttons.html')
def follow(author, target):
    return {
        'is_active': FollowUserDataView.is_following(author, target),
        'target': target,
    }

