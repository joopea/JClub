# Create your views here, but only if they really don't belong anywhere else

from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.template import RequestContext
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.views.generic.base import RedirectView, TemplateView

from apps.suggestions.views import SuggestionListView


def handle_404(request):
    """Makes the 404 pages have the request in the context"""
    html = render_to_string('core/404.html', context_instance=RequestContext(request))
    return HttpResponseNotFound(html)


def handle_500(request):
    """Pass the static url to the 500 error page"""
    html = render_to_string('core/500.html', context_instance=RequestContext(request))
    return HttpResponseServerError(html)


class RedirectToDefaultLanguage(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('home')


class HomeView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        #since this is actually the same as the suggestions, we return that view instead
        suggestions_view = SuggestionListView.as_view()
        return suggestions_view(request, *args, **kwargs)


class DebugView(TemplateView):
    template_name = 'core/dump.html'


class DevelopmentView(TemplateView):
    def get_template_names(self):
        return 'development/{0}.html'.format(self.kwargs['template_name'])


class AjaxFormResponseMixin(object):
    # a mixin to add AJAX support to a form
    # must be used with an object-based FormView (e.g. CreateView)
    success_url = '/'

    def form_invalid(self, form):
        errors = {f: e.get_json_data(False) for f, e in form.errors.items()}
        return JsonResponse(
            {
                'error': errors,
                'success': False,
                'data': {}
            },
            status=400
        )

    def get(self, *args, **kwargs):
        context = self.get_context_data()
        if hasattr(self, 'get_form_class') and callable(self.get_form_class):
            context['form'] = self.get_form_class()
            context['view'] = self
            context.update(csrf(self.request))
            context['form'] = render_to_string(self.template_name, context)
            del context['view']
            del context['csrf_token']

        return JsonResponse(
            {
                'success': True,
                'data': context
            }
        )

    def form_valid(self, form):
        self.object = form.save()
        context = {}
        return JsonResponse(
            {
                'success': True,
                'data': self.get_context_data(**context)
            }
        )

    def delete(self, request, *args, **kwargs):
        super(AjaxFormResponseMixin, self).delete(self, request, *args, **kwargs)
        return JsonResponse(
            {
                'success': True,
                'data': self.get_context_data(**{})
            }
        )

    def get_context_data(self, **kwargs):
        if 'view' in kwargs:
            del kwargs['view']
        return kwargs


class ExtraFormDataMixin(object):
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        if not 'data' in kwargs:
            kwargs['data'] = {}
        if hasattr(kwargs['data'], '_mutable'):
            mutable = kwargs['data']._mutable
            kwargs['data']._mutable = True
        kwargs['data'].update(self.get_extra_data())
        if hasattr(kwargs['data'], '_mutable'):
            kwargs['data']._mutable = mutable
        return form_class(**kwargs)

    def get_extra_data(self):
        return {}


class ModelFormView(object):
    def form_valid(self, form):
        response = super(ModelFormView, self).form_valid(form)
        if hasattr(form, 'after_save') and callable(form.after_save):
            response = form.after_save(response)
        return response
