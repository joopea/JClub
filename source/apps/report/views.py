from django.http import JsonResponse
from django.views.generic import CreateView
from apps.comment.queries import CommentDataView

from apps.core.views import AjaxFormResponseMixin
from apps.post.queries import PostDataView
from lib.behaviours.views import WithAuthor

from .forms import ReportForm


class AjaxCreatePostReportView(WithAuthor, AjaxFormResponseMixin, CreateView):
    template_name = 'report/popup/_new_post.html'
    form_class = ReportForm
    post_id = None
    object = None

    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        self.post_id = self.kwargs['pk']
        return super(AjaxCreatePostReportView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AjaxCreatePostReportView, self).get_context_data(**kwargs)
        context['post'] = self.post_id
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.post_id = self.post_id
        self.object.author = self.request.user
        self.object.save()

        context = {}
        return JsonResponse(
            {
                'success': True,
                'data': self.get_context_data(**context)
            }
        )


class AjaxCreateCommentReportView(WithAuthor, AjaxFormResponseMixin, CreateView):
    template_name = 'report/popup/_new_comment.html'
    form_class = ReportForm
    comment_id = None

    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        self.comment_id = self.kwargs['pk']
        return super(AjaxCreateCommentReportView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AjaxCreateCommentReportView, self).get_context_data(**kwargs)
        context['comment'] = self.comment_id
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.comment_id = self.comment_id
        self.object.author = self.request.user
        self.object.save()

        context = {}
        return JsonResponse(
            {
                'success': True,
                'data': self.get_context_data(**context)
            }
        )
