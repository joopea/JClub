from django import template
from django.template import resolve_variable

register = template.Library()


def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    is_paginated = context['is_paginated']

    if context['page_obj']:
        current_page = context['page_obj'].number
    else:
        current_page = 1

    if context['paginator']:
        number_of_pages = context['paginator'].num_pages
    else:
        number_of_pages = 1

    page_obj = context['page_obj']
    paginator = context['paginator']
    start_page = max(current_page - adjacent_pages, 1)
    end_page = current_page + adjacent_pages + 1

    if end_page > number_of_pages:
        end_page = number_of_pages + 1
    page_numbers = [n for n in range(start_page, end_page) if 0 < n <= number_of_pages]

    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'page': current_page,
        'pages': number_of_pages,
        'page_numbers': page_numbers,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'show_first': 1 not in page_numbers,
        'show_last': number_of_pages not in page_numbers,
        'is_paginated': is_paginated,
        'request': resolve_variable('request', context)
    }

register.inclusion_tag('utils/_pagination.html', takes_context=True)(paginator)
