from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, DeleteView

from apps.core.exceptions import Json404
from apps.core.views import AjaxFormResponseMixin

from lib.behaviours.views import WithAuthor

from .forms import LikePostForm, LikeCommentForm
from .models import LikePost, LikeComment
from apps.comment.queries import CommentLikeCount, CommentDataView
from apps.post.queries import PostLikeCount, PostDataView


class AjaxLikePostCreateView(WithAuthor, AjaxFormResponseMixin, CreateView):

    http_method_names = ['post']

    form_class = LikePostForm
    context_name = 'post'
    data_view = PostDataView

    def get_extra_data(self):
        context = super(AjaxLikePostCreateView, self).get_extra_data()
        context[self.context_name] = self.kwargs.get('pk')
        return context

    def get_context_data(self, **kwargs):
        context = super(AjaxLikePostCreateView, self).get_context_data(**kwargs)

        parent = self.data_view.by_id(self.kwargs.get('pk'))

        context['count'] = parent.like_count

        return context


class AjaxRemoveLikeView(WithAuthor, AjaxFormResponseMixin, DeleteView):
    http_method_names = ['post']

    def get_extra_data(self):
        context = super(AjaxRemoveLikeView, self).get_extra_data()
        context[self.context_name] = self.kwargs.get('pk')
        return context

    def get_object(self, queryset=None):
        args = self.get_extra_data()

        try:
            instance = self.model.objects.get(**args)
        except ObjectDoesNotExist:
            raise Json404()
        return instance

    def delete(self, *args, **kwargs):
        parent = getattr(self.get_object(), self.context_name)

        response = super(AjaxRemoveLikeView, self).delete(*args, **kwargs)

        self.like_count.update(parent)

        return response

    def get_context_data(self, **kwargs):
        context = super(AjaxRemoveLikeView, self).get_context_data(**kwargs)

        parent = self.data_view.by_id(self.kwargs.get('pk'))

        self.like_count.update(parent)

        # Can't use parent.like_count here: not updated on object
        context['count'] = getattr(parent, self.like_relation_attr).count()

        return context


class AjaxLikePostRemoveView(AjaxRemoveLikeView):
    model = LikePost
    context_name = 'post'
    like_count = PostLikeCount
    data_view = PostDataView
    like_relation_attr = 'post_like'


class AjaxLikeCommentCreateView(AjaxLikePostCreateView):
    form_class = LikeCommentForm
    context_name = 'comment'
    data_view = CommentDataView


class AjaxLikeCommentRemoveView(AjaxRemoveLikeView):
    model = LikeComment
    context_name = 'comment'
    like_count = CommentLikeCount
    data_view = CommentDataView
    like_relation_attr = 'likecomment_set'
