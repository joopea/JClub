from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateView
from django.utils.decorators import classonlymethod


class EndlessListPaginatorPage(object):
    has_previous = False
    has_next = True

    def __init__(self, queryset, number, paginator):
        self.object_list = queryset
        self.number = number
        self.paginator = paginator

    def has_other_pages(self):
        return True

    @property
    def next_page_number(self):
        return self.object_list.last_item


class EndlessListPaginator(object):
    num_pages = 99999999
    page_range = []

    def __init__(self, queryset, per_page, **kwargs):
        self.queryset = queryset()
        self.size = per_page

    def page(self, number):
        self.queryset.limit(number, self.size)
        return EndlessListPaginatorPage(self.queryset, number, self)


class EndlessListView(object):
    page_kwarg = 'start'
    paginator_class = EndlessListPaginator
    ajax_template_name = ''

    def get(self, *args, **kwargs):
        if self.request.GET.get('page', None) is not None:
           self.template_name = self.ajax_template_name
        return super(EndlessListView, self).get(*args, **kwargs)


class CollectionList(object):
    def get_context_object_name(self, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(CollectionList, self).get_context_data(**kwargs)
        qs_kwargs = self.get_queryset_kwargs()
        context['object_list'] = context['object_list'].get(**qs_kwargs)
        return context

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]
