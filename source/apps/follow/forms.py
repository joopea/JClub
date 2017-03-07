from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _

from apps.core import forms
from apps.notifications.models import Notification

from .models import FollowUser, FollowCommunity


class WithFollowNotification(object):
    notification_type = 'FOLLOW_USER'
    related_pk_field = 'author'

    def clean(self):
        cleaned_data = super(WithFollowNotification, self).clean()
        if cleaned_data['target'] == cleaned_data['author']:
            raise forms.ValidationError(
                'You cannot follow yourself.',
                code='now-own'
            )
        return cleaned_data

    def get_notification_data(self, instance):
        data = dict()
        data['author'] = self.cleaned_data['author']
        data['owner'] = instance.target
        data['relation_1'] = instance.pk
        data['subject'] = self.notification_type
        return data

    def save(self, *args, **kwargs):
        instance = super(WithFollowNotification, self).save(*args, **kwargs)
        notification = Notification(**self.get_notification_data(instance))
        notification.save()
        return instance


class FollowUserForm(WithFollowNotification, forms.ModelForm):
    class Meta:
        model = FollowUser
        exclude = []
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'You\'re already following this user!'
            }
        }


class FollowCommunityForm(forms.ModelForm):
    class Meta:
        model = FollowCommunity
        exclude = []
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'You\'re already following this community!' 
            }
        }
