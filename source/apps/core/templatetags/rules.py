from django import template

from apps.follow.queries import FollowUserDataView
from apps.like.queries import LikePostDataView, LikeCommentDataView
from apps.save.queries import SavedByUserDataView
from apps.notifications.queries import NotificationDataView

register = template.Library()


class Rules(template.Node):
    def __init__(self, user=None, post=None, comment=None, community=None, wall=None):
        self.user = user
        self.post = post
        self.comment = comment
        self.community = community
        self.post_community = None
        if post and post.community:
            self.post_community = post.community
        self.wall = wall
        self.authenticated = self.user.is_authenticated()
        self.is_post_author = (post and post.author.pk == user.pk)
        self.is_comment_author = (comment and comment.author.pk == user.pk)
        self.is_own_wall = (self.authenticated and self.user == self.wall)

    def render(self, context):
        context['rules'] = self
        return ''

    def is_allowed_on_wall(self):
        if not self.authenticated:
            return False

        if self.community and self.user.is_blocked_by_community(community=self.community):
            return False

        if self.post_community and self.user.is_blocked_by_community(community=self.post_community):
            return False

        if self.wall and self.user.is_blocked_by_user(author=self.wall):
            return False

        # rule for post-detail view, this has no wall,
        # and thus does not check if the viewer is blocked by the post creator
        if not self.wall and self.post and self.user.is_blocked_by_user(author=self.post.author):
            return False

        return True

    def can_like(self):
        return self.authenticated \
            and not self.is_post_author \
            and self.is_allowed_on_wall()

    def has_liked_post(self):
        return self.authenticated \
            and LikePostDataView.is_liked(self.user, self.post)

    def can_share(self):
        return self.authenticated \
            and not self.is_post_author \
            and self.is_allowed_on_wall()

    def has_shared_post(self):
        return self.user.is_authenticated() \
            and NotificationDataView.has_shared(author=self.user.pk, post=self.post.pk)

    def can_follow(self):
        return self.authenticated \
            and not self.post.author.username == 'deleted'\
            and not self.is_post_author

    def following_author(self):
        return self.authenticated \
            and FollowUserDataView.is_following(self.user, self.post.author)

    def can_save(self):
        return self.authenticated

    def has_saved_post(self):
        return self.authenticated \
            and SavedByUserDataView.is_saved(self.user, self.post)

    def can_remove(self):
        return self.is_post_author or self.is_own_wall

    def can_report(self):
        return self.authenticated \
            and not self.is_post_author

    def can_comment(self):
        return self.authenticated \
            and self.is_allowed_on_wall()

    def can_remove_comment(self):
        return self.is_comment_author

    def can_report_comment(self):
        return self.authenticated \
            and not self.is_comment_author

    def can_like_comment(self):
        return self.authenticated \
            and not self.is_comment_author \
            and self.is_allowed_on_wall()

    def has_liked_comment(self):
        return self.authenticated \
            and LikeCommentDataView.is_liked(self.user, self.comment)


@register.assignment_tag
def rules(*args, **kwargs):
    return Rules(**kwargs)
