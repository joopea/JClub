from django.http import Http404
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django import forms
from django.forms import widgets
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from lib.behaviours.views import WithAuthor
from lib.data_views.exceptions import RecordDoesNotExist

from apps.comment.queries import AddPostComments
from apps.core.views import ModelFormView
from apps.core.views import AjaxFormResponseMixin
from apps.menu.views import WithUserMenu
from apps.post.queries import PostShareCount
from apps.wall.queries import WallPostDataView

from .models import Post
from .forms import PostForm


class PostDetail(WithUserMenu, DetailView):
    template_name = 'post/post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['is_expanded'] = True

        AddPostComments.all(post=self.object)

        return context


class PostCreate(WithAuthor, ModelFormView, AjaxFormResponseMixin, CreateView):
    template_name = 'post/popup/_new.html'
    form_class = PostForm

    http_method_names = ['get', 'post']

    def get_context_data(self):
        if hasattr(self, 'object'):
            if self.object.needs_approval:
                return {'approval': _('This post is sent for approval because: {0}').format(unicode(self.object.dis_approval_reasons))}
        return {}


"""
    GET op AjaxModelFormDeleteView geeft ajax response met {"form": <html form>}
        is een ModelForm

    POST op AjaxModelFormDeleteView validate form met ge-submitte data
        als data invalid:
            http 400, {"form": <html form met errors>}
        anders
            http 200, {"success": true, "data": {"message": "<text|object>"}

"""


class ButtonChoicesWidget(widgets.Input):
    input_type = 'submit'

    def __init__(self, attrs=None, choices=()):
        if attrs is not None:
            self.input_type = attrs.pop('type', self.input_type)
        super(ButtonChoicesWidget, self).__init__(attrs)
        self.choices = choices

    def render(self, name, value, attrs=None):
        out = format_html('<span{}>', flatatt(self.build_attrs(attrs)))
        for choice in self.choices:
            out += super(ButtonChoicesWidget, self).render(choice[0], choice[1],
                                                           self.build_attrs(attrs, type=self.input_type, name=name))
        return mark_safe(out + '</span>')


class ButtonChoicesField(forms.ChoiceField):
    widget = ButtonChoicesWidget


class AjaxModelFormDeleteView(AjaxFormResponseMixin, UpdateView):
    def __init__(self, *args, **kwargs):
        self.model = self.form_class._meta.model
        super(AjaxModelFormDeleteView, self).__init__(*args, **kwargs)


class PostDeleteForm(forms.ModelForm):
    YES = 'Yes, delete post'
    NO = 'No'

    CHOICES = (
        (YES, YES),
        (NO, NO)
    )

    yes_no = ButtonChoicesField(choices=CHOICES, label=_('Are you sure you want to delete this post?'), required=True)

    def save(self, commit=True):
        if self.cleaned_data['yes_no'] == self.YES:
            # if this post in on this user's wall and the user is not the owner of this post
            # remove the post from this user's wall
            try:
                wall_post = WallPostDataView.get(user_id=self.data.get('author', 0), post_id=self.instance.pk)
                wall_post.delete()

                PostShareCount.update(self.instance)
            except RecordDoesNotExist:
                raise Http404

            # if the post is owned by this user, delete the post (and let it cascade)
            if self.data.get('author', 0) == self.instance.author.pk:
                self.instance.delete()

        return self.instance

    class Meta:
        model = Post
        fields = (
            'id',
        )


class PostDelete(WithAuthor, AjaxModelFormDeleteView):
    template_name = 'post/popup/_delete.html'
    form_class = PostDeleteForm

    def __init__(self, *args, **kwargs):
        self.is_deleted = False
        super(PostDelete, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        self.is_deleted = bool(str(form.data['yes_no']) == str(form.YES))
        return super(PostDelete, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs = super(PostDelete, self).get_context_data(**kwargs)
        kwargs['valid'] = self.is_deleted
        return kwargs
