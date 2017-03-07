from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _

from apps.comment.queries import CommentLikeCount
from apps.core import forms
# from apps.core.forms.constraints import WithOwnerIsNotSelfConstraint
# from apps.notifications.forms import WithLikeNotification
from apps.notifications.models import Notification
from apps.post.queries import PostLikeCount

from .models import LikePost, LikeComment


class WithLikeNotification(object):
    notification_type = 'LIKE'
    related_pk_field = ''

    def clean(self):
        cleaned_data = super(WithLikeNotification, self).clean()
        instance = self.get_object(cleaned_data)
        if instance.author == cleaned_data['author']:
            raise forms.ValidationError(
                _('You cannot like this {0}, since you are the creator of this {1}'.format(
                    self.related_pk_field, self.related_pk_field
                )),
                code='now-own'
            )
        return cleaned_data

    def get_notification_data(self, instance):
        data = dict()
        data['author'] = self.cleaned_data['author']
        data['owner'] = instance.post.author
        data['relation_1'] = instance.post.id
        data['subject'] = self.notification_type
        return data

    def save(self, *args, **kwargs):
        instance = super(WithLikeNotification, self).save(*args, **kwargs)
        notification = Notification(**self.get_notification_data(instance))
        notification.save()
        return instance


class LikeForm(WithLikeNotification, forms.ModelForm):
    def get_object(self, cleaned_data):
        return cleaned_data[self.related_pk_field]


class LikePostForm(LikeForm):
    notification_type = 'LIKE_POST'
    related_pk_field = 'post'

    class Meta:
        model = LikePost
        exclude = []
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _('You already liked this post!')
            }
        }

    def save(self, *args, **kwargs):
        instance = super(LikeForm, self).save(*args, **kwargs)

        PostLikeCount.update(instance.post)

        return instance


class LikeCommentForm(LikeForm):
    notification_type = 'LIKE_COMMENT'
    related_pk_field = 'comment'

    class Meta:
        model = LikeComment
        exclude = []
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _('You already liked this comment')
            }
        }

    def save(self, *args, **kwargs):
        instance = super(LikeForm, self).save(*args, **kwargs)

        CommentLikeCount.update(instance.comment)

        return instance

    def get_notification_data(self, instance):
        data = dict()
        data['author'] = self.cleaned_data['author']
        data['owner'] = instance.comment.author
        data['relation_1'] = instance.comment.post.id
        data['subject'] = self.notification_type
        return data
