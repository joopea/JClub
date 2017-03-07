from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from apps.post.queries import PostDataView

from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withuser import WithAuthor


class Notification(WithUpdates, WithAuthor, models.Model):

    LIKE_POST = 'LIKE_POST'
    LIKE_COMMENT = 'LIKE_COMMENT'
    MENTION_POST = 'MENTION_POST'
    MENTION_COMMENT = 'MENTION_COMMENT'
    FOLLOW_USER = 'FOLLOW_USER'
    POST_COMMENT = 'POST_COMMENT'
    SHARE_POST = 'SHARE_POST'
    FOLLOWEE_SHARE_POST = 'FOLLOWEE_SHARE_POST'
    COMMENT_AFTER_COMMENT = 'COMMENT_AFTER_COMMENT'
    DISSAPROVED_POST = 'DISSAPROVED_POST'
    DISSAPROVED_COMMENT = 'DISSAPROVED_COMMENT'
    APPROVED_REPORTED_POST = 'APPROVED_REPORTED_POST'
    DISAPPROVED_REPORTED_POST = 'DISAPPROVED_REPORTED_POST'
    APPROVED_REPORTED_COMMENT = 'APPROVED_REPORTED_COMMENT'
    DISAPPROVED_REPORTED_COMMENT = 'DISAPPROVED_REPORTED_COMMENT'
    DELETED_COMMENT = 'DELETED_COMMENT'
    DELETED_POST = 'DELETED_POST'
    WARNING = 'WARNING'

    NOTIFICATION_CHOICES = (
        (LIKE_POST, _('liked your post')),
        (LIKE_COMMENT, _('liked your comment in post')),
        (MENTION_POST, _('mentioned you in')),
        (MENTION_COMMENT, _('mentioned you in a comment at')),
        (FOLLOW_USER, _('is now following you')),
        (POST_COMMENT, _('commented on')),
        (SHARE_POST, _('shared a post with you')),
        (COMMENT_AFTER_COMMENT, _('commented on a post you commented on')),
        # notification happens when sharing someone's post, that user gets this notification
        # <user-id> shared your post <post title>
        (FOLLOWEE_SHARE_POST, _('shared your post')),
        (DISSAPROVED_POST, _('dissaproved your post')),
        (DISSAPROVED_COMMENT, _('dissaproved your comment')),
        (APPROVED_REPORTED_POST, _('reported and removed your post')),
        (DISAPPROVED_REPORTED_POST, _('disapproved your report on')),
        (APPROVED_REPORTED_COMMENT, _('reported and removed your comment')),
        (DISAPPROVED_REPORTED_COMMENT, _('disapproved your report on a comment at')),
        (DELETED_COMMENT, _('deleted your comment')),
        (DELETED_POST, _('deleted your post')),
        (WARNING, _('warning')),
    )

    POST_NOTIFICATIONS = [LIKE_POST, LIKE_COMMENT, MENTION_POST, MENTION_COMMENT, POST_COMMENT, SHARE_POST,
                          FOLLOWEE_SHARE_POST, DISAPPROVED_REPORTED_POST, DISAPPROVED_REPORTED_COMMENT,
                          COMMENT_AFTER_COMMENT, DELETED_COMMENT]
    WARNING_TYPES = [WARNING, DISAPPROVED_REPORTED_COMMENT, DISAPPROVED_REPORTED_POST, DISSAPROVED_POST,
                     DISSAPROVED_COMMENT]

    owner = models.ForeignKey('users.User', related_name='target', help_text=_("The user getting the notification"))
    read = models.BooleanField(default=False)

    subject = models.CharField(max_length=1024, choices=NOTIFICATION_CHOICES, help_text=_("The notification subject"))

    relation_1 = models.IntegerField(help_text=_("Relation (pk) to the notified object, leave 0 if not used"), default=0)
    relation_2 = models.IntegerField(blank=True, null=True, default=None)
    original = models.CharField(_('Message'), max_length=4096, blank=True, null=True, default=None)

    def __unicode__(self):
        return 'Notification {0} from {1} to: {2}'.format(unicode(self.subject), unicode(self.author), unicode(self.owner))

    @property
    def is_warning(self):
        return True if self.subject in self.WARNING_TYPES else False

    def get_template(self):
        """
        Django takes the first template which matches the template key. The second template thus acts as a default

        The type of notification is used as template key. If you want to add a new notification, simply add a key
        and new template with corresponding name.
        """

        return render_to_string((
            'notifications/includes/notification_%s.html' % self.subject.lower(),
            'notifications/includes/notification.html',
        ), {'content': self})

    def render(self):
        return self.get_template()

    def get_absolute_url(self):
        if self.subject in self.POST_NOTIFICATIONS:
            try:
                return reverse("post:detail", kwargs={"pk": self.relation_1})
            except NoReverseMatch:
                pass

        return '/'

    def get_target_title(self):

        if self.subject in self.POST_NOTIFICATIONS:
            post = PostDataView.by_id(self.relation_1)  # Todo: Store post title as text, when creating notification
            if post:
                return post.title
            else:
                return 'Post not found'

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created']
