from django.contrib.admin.views.main import ChangeList
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from apps.custom_admin.admin import ButtonableAdmin, ImprovedRawIdFields
from apps.notifications.queries import NotificationDataView
from apps.post.forms import PostForm
from apps.comment.forms import CommentForm

from .models import CommentApproval, PostApproval


class AlwaysApprove(object):
    def check_published(self, *args, **kwargs):
        return True

    def clean(self, *args, **kwargs):
        pass

    def bleach(self, *args, **kwargs):
        pass


class AdminCommentForm(AlwaysApprove, CommentForm):
    pass


class AdminPostForm(AlwaysApprove, PostForm):
    pass


class CommentApprovalAdmin(ButtonableAdmin, ImprovedRawIdFields):
    return_url = reverse_lazy("admin:approval_commentapproval_changelist")
    search_fields = ['comment__post__title', 'comment__author__username']
    list_display = ['reason', 'image_thumbnail', 'get_link', 'get_author', 'approve_show', 'disapprove_show', 'get_created']
    raw_id_fields = ['comment']
    readonly_fields = ['reason']
    fields = ['comment', 'reason']
    raw_id_managers = {'comment': 'all_objects'}

    def get_link(self, obj):
        return '<a href="{0}">{1}</a>'.format(reverse_lazy("admin:comment_comment_change", args=[obj.comment_id]), obj.comment)

    get_link.short_description = _('Comment')
    get_link.allow_tags = True

    def get_author(self, obj):
        return obj.comment.author

    get_author.short_description = _('Author')
    get_author.admin_order_field = 'comment__author'

    def get_created(self, obj):
        return obj.comment.created

    get_created.short_description = _('Created')
    get_created.admin_order_field = 'comment__created'

    @method_decorator(staff_member_required)
    def approve(self, request, obj):
        obj.approve()
        form = AdminCommentForm(
            data={
                'author': obj.comment.author.id,
                'message': obj.comment.message,
                'post': obj.comment.post.id
            },
            instance=obj.comment
        )
        if form.is_valid():
            form.save()
        return redirect(self.return_url)

    approve.short_description = _('Approve')

    @method_decorator(staff_member_required)
    def disapprove(self, request, obj):
        obj.disapprove()
        NotificationDataView.approval_notification(request.user, obj.comment.author, NotificationDataView.get_model().DISSAPROVED_COMMENT)
        return redirect(self.return_url)

    disapprove.short_description = _('Disapprove')

    def approve_show(self, obj):
        return '<a class="addlink" href="{0}/approve">Approve</a>'.format(obj.id)

    approve_show.allow_tags = True
    approve_show.short_description = _("Approve")

    def disapprove_show(self, obj):
        return '<a class="deletelink" href="{0}/disapprove">Disapprove</a>'.format(obj.id)

    disapprove_show.allow_tags = True
    disapprove_show.short_description = _("Disapprove")

    def image_thumbnail(self, obj):
        return render_to_string('approval/_admin_thumbnail.html', context={"image": obj.get_image()})

    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = _("Image")

    """
    Declare your admin buttons here!
    """
    buttons = [(approve.func_name, approve.short_description), (disapprove.func_name, disapprove.short_description), ]


class PostApprovalAdmin(ButtonableAdmin, ImprovedRawIdFields):
    return_url = reverse_lazy("admin:approval_postapproval_changelist")
    search_fields = ['post__title', 'post__author__username']
    list_display = ['reason', 'image_thumbnail', 'get_link', 'get_author', 'approve_show', 'disapprove_show', 'get_created']
    raw_id_fields = ['post']
    readonly_fields = ['reason']
    fields = ['post', 'reason']
    raw_id_managers = {'post': 'all_objects'}

    def get_link(self, obj):
        return '<a href="{0}">{1}</a>'.format(reverse_lazy("admin:post_post_change", args=[obj.post_id]), obj.post)

    get_link.short_description = _('Post')
    get_link.allow_tags = True

    def get_author(self, obj):
        return obj.post.author

    get_author.short_description = _('Author')
    get_author.admin_order_field = 'post__author'

    def get_created(self, obj):
        return obj.post.created

    get_created.short_description = _('Created')
    get_created.admin_order_field = 'post__created'

    @method_decorator(staff_member_required)
    def approve(self, request, obj):
        obj.approve()
        data = {
            'author': obj.post.author.id,
            'message': obj.post.message,
            'title': obj.post.title,
            'community': obj.post.community_id
        }
        if obj.post.community:
            data['wall-selector'] = 'community'
        form = AdminPostForm(
            data=data,
            instance=obj.post
        )
        if form.is_valid():
            form.save()
        return redirect(self.return_url)

    approve.short_description = _('Approve')

    @method_decorator(staff_member_required)
    def disapprove(self, request, obj):
        obj.disapprove()
        NotificationDataView.approval_notification(request.user, obj.post.author, NotificationDataView.get_model().DISSAPROVED_POST)
        return redirect(self.return_url)

    disapprove.short_description = _('Disapprove')

    def approve_show(self, obj):
        return '<a class="addlink" href="{0}/approve">Approve</a>'.format(obj.id)

    approve_show.allow_tags = True
    approve_show.short_description = _("Approve")

    def disapprove_show(self, obj):
        return '<a class="deletelink" href="{0}/disapprove">Disapprove</a>'.format(obj.id)

    disapprove_show.allow_tags = True
    disapprove_show.short_description = _("Disapprove")

    def image_thumbnail(self, obj):
        return render_to_string('approval/_admin_thumbnail.html', context={"image": obj.get_image()})

    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = _("Image")

    """
    Declare your admin buttons here!
    """
    buttons = [(approve.func_name, approve.short_description), (disapprove.func_name, disapprove.short_description), ]

admin.site.register(CommentApproval, CommentApprovalAdmin)
admin.site.register(PostApproval, PostApprovalAdmin)
