from django.utils.translation import ugettext_lazy as _
from django import forms
from django.db.models import ObjectDoesNotExist

from apps.core import forms as core_forms
from apps.core.detectors import WithPhonenumberDetection, WithEmailDetection, WithRealnameDetection, \
    WithImageApprovalCheck
from apps.image.forms import WithImage
from apps.mention.forms import WithMentions
from apps.notifications.queries import NotificationDataView

from apps.post.forms import WithRichTextContent
from apps.post.queries import PostCommentCount
from apps.post.views import ButtonChoicesField

from .models import Comment
from .queries import CommentDataView
from apps.approval.forms import WithApprovalCheck


class WithCommentNotification(object):
    notification_type = 'POST_COMMENT'
    related_pk_field = ''

    def get_comment_notification_data(self, instance):
        data = dict()
        data['author'] = self.cleaned_data.get('author')
        data['owner'] = instance.post.author
        data['relation_1'] = instance.post.id
        data['subject'] = self.notification_type
        return data

    def get_comment_after_comment_data(self, instance):
        try:
            data = dict()
            latest = CommentDataView.last(instance.post.id)
            data['author'] = self.cleaned_data.get('author')
            data['owner'] = latest.author
            data['relation_1'] = instance.post.id
            data['subject'] = 'COMMENT_AFTER_COMMENT'
            if data['author'].pk != data['owner'].pk:
                return data
        except ObjectDoesNotExist:
            pass
        return None

    def save(self, *args, **kwargs):
        instance = super(WithCommentNotification, self).save(*args, **kwargs)
        NotificationDataView.add(**self.get_comment_notification_data(instance))
        comment_after_comment = self.get_comment_after_comment_data(instance)
        if comment_after_comment:
            NotificationDataView.add(**comment_after_comment)
        return instance


class CommentForm(WithApprovalCheck, WithPhonenumberDetection, WithEmailDetection, WithRealnameDetection,
                  WithImageApprovalCheck, WithRichTextContent, WithMentions, WithImage, WithCommentNotification,
                  core_forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            'message',
            'post',
            'author',
        )

    def save(self, *args, **kwargs):
        comment = super(CommentForm, self).save(*args, **kwargs)

        PostCommentCount.update(comment.post)

        if self.has_disapproval_reasons:
            comment.needs_approval = True
            comment.dis_approval_reasons = self.get_disapproval_reasons()

        return comment


class CommentDeleteForm(forms.ModelForm):
    YES = 'Yes, delete comments'
    NO = 'No'

    CHOICES = (
        (YES, YES),
        (NO, NO)
    )

    yes_no = ButtonChoicesField(choices=CHOICES, label=_('Are you sure you want to delete this?'), required=True)

    def save(self, commit=True):
        if self.cleaned_data['yes_no'] == self.YES:
            post = self.instance.post

            self.instance.delete()

            # Count comments after deleting this one. Otherwise count is off by one
            PostCommentCount.update(post)
        return self.instance

    class Meta:
        model = Comment
        fields = (
            'id',
        )
