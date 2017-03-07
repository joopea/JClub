from django.core.exceptions import NON_FIELD_ERRORS, ObjectDoesNotExist
from django.utils.translation import ugettext as _

from apps.core import forms
from apps.users.models import User

from .models import Mention
from .functions import find_mentions

"""
A User receives a Notification if he/she is Mentioned in a Post
A User receives a Notification if he/she is Mentioned in a Comment
"""
from apps.notifications.forms import WithMentionNotification

"""
A User(A) can Mention any other User(B) if User(B) didn't block User(A)
If a User(a) is Blocked by another User(b) and User(a) Mentions that User(b) in a Post nothing happens
User(a) can't mention user(b) if user(b) blocked user(a). An error should be shown
If a User(a) is Blocked by another User(b) and User(a) Mentions that User(b) in a Comment nothing happens
Same above rule
"""
from apps.core.forms.constraints import WithAuthorNotBlockedByTarget

from apps.wall.forms import WallForm


class MentionForm(WithMentionNotification, WithAuthorNotBlockedByTarget, forms.ModelForm):
    """
    core ModelForm first, Constraints second, actions last
    """
    class Meta:
        model = Mention
        exclude = []
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _('You\'ve already mentioned this user!')
            }
        }


class WithMentions(object):
    """
    find all mentions in the response from <whatever>.get_message() (should be a string)
    for all mentions a MentionForm is filled and saved
        each mention will in turn trigger the corresponding actions required.
    """
    def __init__(self, *args, **kwargs):
        super(WithMentions, self).__init__(*args, **kwargs)
        self.mentions = []
        self.mentioned_users = {}

    def get_message(self):
        return self.cleaned_data.get('message', '')

    def get_title(self):
        return self.cleaned_data.get('title', '')

    def handle_mentions(self, content):
        mentions = set(find_mentions(content))

        # In order to be able to validate the mentions we need to create the instances without committing here
        # later in save we can commit them
        for mention in mentions:
            try:
                target = User.objects.get(username=mention.replace('@', ''))
                self.mentioned_users[mention] = target.get_absolute_url()
            except ObjectDoesNotExist:
                output = _('You have mentioned a non-existing user (%s)') % (unicode(mention.replace('@', ''), ))
                self.add_error('message', output)
                break
            instance = MentionForm(data={
                'author': self.cleaned_data['author'].pk,
                'author_name': self.cleaned_data['author'].username,
                'target': target.pk,
                'target_name': target.username,
            })
            if not instance.is_valid():
                # add to form errors
                output = _('You are blocked by the user you`ve mentioned (%s)') % (unicode(mention.replace('@', ''), ))
                self.add_error('message', output)
                break
            self.mentions.append(instance)

    def clean(self):
        cleaned_data = super(WithMentions, self).clean()

        message = self.get_message()
        self.handle_mentions(message)

        title = self.get_title()
        if title:
            self.handle_mentions(title)

        return cleaned_data

    def save(self, *args, **kwargs):
        if self.instance.pk is None:
            for mention, url in self.mentioned_users.iteritems():
                self.instance.message = self.instance.message.replace(
                    mention, u'<a href="' + url + u'">' + mention + u'</a>'
                )
            # if hasattr(self.instance, 'title'):
            #     for mention, url in self.mentioned_users.iteritems():
            #         self.instance.title = self.instance.title.replace(
            #             mention, '<a href="' + url + '">' + mention.encode('utf-8') + '</a>'
            #         )
        instance = super(WithMentions, self).save(*args, **kwargs)
        return instance

    def after_save(self, response):
        response = super(WithMentions, self).after_save(response)
        for mention in self.mentions:
            if self.instance.__class__.__name__ == 'Post':
                mention.post = self.instance.id
                # add the post to the mentioned user's wall (US 197)
                w = WallForm(data={'post': self.instance.id, 'author': mention.data['target']})
                if w.is_valid():
                    w.save()
            if self.instance.__class__.__name__ == 'Comment':
                mention.post = self.instance.post.id
                mention.comment = True
            mention.save()

        return response
