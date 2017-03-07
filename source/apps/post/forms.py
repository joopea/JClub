import re
import logging
import bleach
import json
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms.util import ErrorList

from lib.behaviours.views.formview import WithGenericForeignKey

from apps.approval.forms import WithApprovalCheck
from apps.core import forms as core_forms
from apps.core.detectors import WithPhonenumberDetection, WithEmailDetection, WithRealnameDetection, \
    WithImageApprovalCheck
from apps.follow.queries import FollowersCommunityDataView, FollowUserDataView
from apps.image.forms import WithImage
from apps.mention.forms import WithMentions
from apps.post.queries import PostShareCount
from apps.users.models import User
from apps.wall.forms import WallForm
from apps.notifications.queries import NotificationDataView

from .models import Post
from apps.shorturl.queries import ShortURLDataView

LOG = logging.getLogger('shorturl')

# https://gist.github.com/imme-emosol/731338/810d83626a6d79f40a251f250ed4625cac0e731f
# find_url_re = re.compile(r'^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$')
# https://gist.github.com/uogbuji/705383
GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')


def get_urls(s):
    """
    Returns an iterator of matched emails found in string s.
    sort on match length, so replacing a shorter url does not replace a sub-match of a longer one
    """
    def sorter(left, right):
        return len(right) - len(left)

    result = list((url[0] for url in re.findall(GRUBER_URLINTEXT_PAT, s)))
    result.sort(cmp=sorter)
    return result


# A Post content consisting of a link will be served by an external domain that serves as a RedirectService
class WithRichTextContent(object):
    def __init__(self, *args, **kwargs):
        super(WithRichTextContent, self).__init__(*args, **kwargs)
        self.urls = []

    def clean(self, *args, **kwargs):
        cleaned_data = super(WithRichTextContent, self).clean(*args, **kwargs)
        message = cleaned_data.get('message', '')
        if message:
            self.urls = get_urls(message.replace('&nbsp;', ' '))
        return cleaned_data

    def bleach(self):
        self.instance.message = self.instance.message.strip()
        if self.instance.message.startswith('<p>'):
            self.instance.message = self.instance.message[3:]
        if self.instance.message.endswith('</p>'):
            self.instance.message = self.instance.message[:-4]
        # only for comments, replace line-breaks with <br/> so they remain
        self.instance.message = self.instance.message.replace('\n', '<br>')
        self.instance.message = bleach.clean(self.instance.message, **settings.BLEACH_CONFIG)
        self.instance.message = self.instance.message.replace('&nbsp;', ' ')
        self.instance.message = self.instance.message.replace('<br>', '<br />')
        self.instance.message = self.instance.message.replace('<br /><br />', '<br />')
        self.instance.original_message = self.cleaned_data['message']

        if hasattr(self.instance, 'title'):
            self.instance.title = self.instance.title.strip()
            self.instance.title = bleach.clean(self.instance.title, **settings.BLEACH_CONFIG)
            self.instance.title = self.instance.title.replace('&nbsp;', ' ')

    def save(self, *args, **kwargs):
        replacements = []
        if self.instance.pk is None:
            self.bleach()
            # collect replacements
            for url in self.urls:
                replacements.append(ShortURLDataView.get_or_create(long=url))
                # fill in stubs while replacing ("ABC" will be replaced by "<a href='sdsd'>ABC</a>")
                # if we leave the replaced value a "shorter" match will replace it again
                self.instance.message = self.instance.message.replace(url, '__||' + str(replacements[-1].pk) + '||__')
            # here the message is replaced for each url by its key,
            # for example "__||4762c372-d02d-435a-a2b2-16a23201e14e||__"
            for replacement in replacements:
                self.instance.message = self.instance.message.replace(
                    '__||' + str(replacement.pk) + '||__',
                    '<a href="' + replacement.url + '">' + replacement.long + '</a>'
                )
        instance = super(WithRichTextContent, self).save(*args, **kwargs)
        return instance


class PostForm(WithApprovalCheck, WithPhonenumberDetection, WithEmailDetection, WithRealnameDetection,
               WithImageApprovalCheck, WithRichTextContent, WithMentions, WithImage, WithGenericForeignKey,
               core_forms.ModelForm):

    def clean(self):
        if self.data.get('wall-selector', '') == 'other':
            user = User.objects.filter(username=self.data.get('wall', ''))
            if not user.exists():
                raise core_forms.forms.ValidationError('User could not be found', 'user_not_found')
            # if self.user.is_blocked_by_user(author=self.wall):
            if len(user) and User(pk=self.data['author']).is_blocked_by_user(author=user[0]):
                if 'wall' not in self._errors:
                    self._errors['wall'] = ErrorList()
                self._errors['wall'].append('You are blocked by this user')
        if self.data.get('wall-selector', '') != 'community':
            self.cleaned_data['community'] = None
        if self.cleaned_data['community'] and \
                self.cleaned_data['author'].is_blocked_by_community(self.cleaned_data['community']):
            if 'community' not in self._errors:
                self._errors['community'] = ErrorList()
            self._errors['community'].append('You are blocked from posting on this community')
        super(PostForm, self).clean()

    # post-meta data
    #   wall-selector
    #   community   (is submitted when wall-selector === 'community'    eg. a community wall)
    #   wall        (is submitted when wall-selector === 'other'        eg. another user's wall)
    # we need to save the post meta-data on creation when moderation is required, otherwise reconstructing
    # the circumstances when the post was created is impossible
    #
    # {"wall-selector": "community"}                30
    # {"wall-selector": "own"}                      24
    # {"wall-selector": "other", "target": <id>}    72

    def save(self, *args, **kwargs):

        if self.instance.pk is None:
            # add meta-data to post
            meta = {
                "wall-selector": self.data.get('wall-selector', '')
            }
            if self.data.get('wall-selector', '') == 'other':
                target = User.objects.get(username=self.data.get('wall', ''))
                meta['target'] = target.pk
            self.instance.meta = json.dumps(meta)
        else:
            meta = json.loads(self.instance.meta)

        post = super(PostForm, self).save(*args, **kwargs)

        # handle published posts
        if post.published:
            # add this post to all users following the post author
            author_followers = FollowUserDataView.followers(post.author.pk)
            for follower in author_followers:
                wall_form = WallForm(data={'post': post.pk, 'is_read': False, 'author': follower.author.pk})
                if wall_form.is_valid():
                    wall_form.save()
                    # create a notification for each user that this post is shared to
                    NotificationDataView.create_share_post_notification(
                        author=post.author,
                        target=follower.author,
                        post_id=post.pk
                    )

            # save to Author's wall
            WallForm(data={'post': post.pk, 'author': post.author.pk}).save()
            if meta['wall-selector'] == 'other':
                # save to target user's wall
                wf = WallForm(data={'post': post.pk, 'is_read': False, 'author': meta['target']})
                # check and ignore invalid because the user could have been deleted between post creation and moderation
                if wf.is_valid():
                    wf.save()
                    # create notification that someone posted on target user's wall
                    NotificationDataView.create_post_on_user_wall_notification(
                        author=post.author,
                        target_id=meta.get('target', 0),
                        post_id=post.pk
                    )
            if meta['wall-selector'] == 'community' and post.community:
                # add this post to all users following this community
                followers = FollowersCommunityDataView.list(community_id=post.community.id)
                for follower in followers:
                    wall_form = WallForm(data={'post': post.pk, 'is_read': False, 'author': follower.id})
                    if wall_form.is_valid():
                        wall_form.save()

        PostShareCount.update(post)

        if self.has_disapproval_reasons:
            post.needs_approval = True
            post.dis_approval_reasons = self.get_disapproval_reasons()

        return post

    class Meta:
        model = Post
        fields = (
            'message',
            'title',
            'community',
            'author',
            # 'image'
        )
