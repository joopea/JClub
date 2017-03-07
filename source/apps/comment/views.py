from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.translation import ugettext_lazy as _

from apps.core.views import ModelFormView, AjaxFormResponseMixin, ExtraFormDataMixin
from lib.behaviours.views import WithAuthor

from .forms import CommentForm, CommentDeleteForm
from .queries import CommentDataView
from apps.post.queries import PostDataView


class WithPost(ExtraFormDataMixin):
    def get_extra_data(self, *args, **kwargs):
        context = super(WithPost, self).get_extra_data(*args, **kwargs)
        context['post'] = self.kwargs['pk']
        return context


class CommentCreate(WithAuthor, WithPost, ModelFormView, AjaxFormResponseMixin, CreateView):
    template_name = 'post/popup/_new.html'
    comment_template_name = 'comment/_comment.html'

    form_class = CommentForm

    http_method_names = ['get', 'post']

    def form_valid(self, form):
        obj = form.save()

        if hasattr(form, 'after_save') and callable(form.after_save):
            obj = form.after_save(obj)
        context = {
            'view': self,
            'request': self.request,
            'comment': obj,
            'post': obj.post,
        }
        data = {
            'comment': render_to_string(self.comment_template_name, context),
            'count': obj.post.comment_set.count()
        }

        if obj.needs_approval:
            data['approval'] = _('This comment is sent for approval because: %s. A preview is visible only to you') % obj.dis_approval_reasons.decode("utf8")

        return JsonResponse(
            {
                'success': True,
                'data': data
            }
        )


class FirstAndLastComments(AjaxFormResponseMixin, ListView):
    template_name = 'comment/_first_last.html'
    queryset = CommentDataView
    page_size = 5

    def get_queryset(self):
        # Dict: {first: [comments], last: [comments], remaining: int}
        result = self.queryset.first_and_last(post_id=self.post.id)

        self.remaining = result['remaining']
        if self.remaining:
            self.start_id = result['first'][1].id
            self.end_id = result['last'][0].id

        return result

    def get_context_data(self, **kwargs):
        context = super(FirstAndLastComments, self).get_context_data(**kwargs)
        context['view'] = self
        context['comments'] = self.get_queryset()
        context['request'] = self.request
        context['remaining'] = self.remaining
        context['page_size'] = min(self.page_size, self.remaining)
        context['post_id'] = self.post.id
        if self.post.community:
            context['community'] = self.post.community
        context['start_id'] = getattr(self, 'start_id', None)
        context['end_id'] = getattr(self, 'end_id', None)

        return context

    def get(self, *args, **kwargs):
        self.post = PostDataView.by_id(post_id=self.kwargs['pk'])

        if self.request.user.is_anonymous() and self.post.community is None:
            raise PermissionDenied()

        if not settings.DEBUG and not self.request.is_ajax():
            raise PermissionDenied()

        html = render_to_string(self.template_name, self.get_context_data())

        return JsonResponse(
            {
                'success': True,
                'data': {
                    'comments': html,
                }
            }
        )


class CommentList(AjaxFormResponseMixin, ListView):
    template_name = 'comment/list.html'
    queryset = CommentDataView
    page_size = 5

    def get_queryset(self):
        opts = {
            'post_id': self.post.id,
            'start_id': self.request.GET.get('s', None),
            'end_id': self.request.GET.get('e', None),
            'page_size': self.page_size,
        }

        result = self.queryset.post_page(**opts)

        self.remaining = result['remaining']

        if self.remaining:
            self.start_id = result['comments'][-1].id

        return result

    def get_context_data(self, **kwargs):
        context = super(CommentList, self).get_context_data(**kwargs)
        context['view'] = self
        context['comments'] = self.get_queryset()
        context['request'] = self.request
        context['remaining'] = self.remaining
        context['page_size'] = min(self.page_size, self.remaining)
        context['start_id'] = getattr(self, 'start_id', None)
        context['end_id'] = self.request.GET.get('e', None)
        context['post_id'] = self.kwargs.get('pk', None)

        return context

    def get(self, *args, **kwargs):
        self.post = PostDataView.by_id(post_id=self.kwargs['pk'])

        if self.request.user.is_anonymous() and self.post.community is None:
            raise PermissionDenied()

        if not settings.DEBUG and not self.request.is_ajax():
            raise PermissionDenied()

        html = render_to_string(self.template_name, self.get_context_data())

        return JsonResponse(
            {
                'success': True,
                'data': {
                    'comments': html,
                }
            }
        )


class AjaxModelFormDeleteView(AjaxFormResponseMixin, UpdateView):
    def __init__(self, *args, **kwargs):
        self.model = self.form_class._meta.model
        super(AjaxModelFormDeleteView, self).__init__(*args, **kwargs)


class CommentDelete(WithAuthor, AjaxModelFormDeleteView):
    template_name = 'comment/popup/_delete.html'
    form_class = CommentDeleteForm

    def __init__(self, *args, **kwargs):
        self.is_deleted = False
        super(CommentDelete, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        self.is_deleted = bool(str(form.data['yes_no']) == str(form.YES))
        self.post = form.instance.post
        return super(CommentDelete, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs = super(CommentDelete, self).get_context_data(**kwargs)
        kwargs['valid'] = self.is_deleted
        if self.request.method == 'POST':
            kwargs['count'] = self.post.\
                comment_set.\
                count()
        return kwargs
