from django.views.generic import FormView

from apps.core.views import AjaxFormResponseMixin

from lib.behaviours.views import WithAuthor

from .forms import ShareForm

from apps.post.queries import PostDataView


class AjaxCreateShareView(WithAuthor, AjaxFormResponseMixin, FormView):
    template_name = 'share/popup/_new.html'

    http_method_names = ['get', 'post']

    form_class = ShareForm

    def get_extra_data(self, **kwargs):
        context = super(AjaxCreateShareView, self).get_extra_data()
        context['post'] = self.kwargs.get('pk')
        return context

    def get_context_data(self, **kwargs):
        context = super(AjaxCreateShareView, self).get_context_data(**kwargs)

        context['count'] = PostDataView.by_id_or_404(self.kwargs.get('pk')).share_count

        return context
