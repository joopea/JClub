from lib.data_views import DataViewSourceMixin, DataViewMultipleObjectMixin, DataViewSingleObjectMixin
from apps.notifications.queries import NotificationDataView


class CommunityWallDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'wall'
    model = 'CommunityWall'


class WallDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'users'
    model = 'User'


class WallPostDataView(DataViewSourceMixin, DataViewMultipleObjectMixin, DataViewSingleObjectMixin):
    app_name = 'wall'
    model = 'Wall'

    @classmethod
    def get(cls, user_id=None, post_id=None):
        return super(WallPostDataView, cls).get(author_id=user_id, post_id=post_id)

    @classmethod
    def add_readstatus_to_posts(cls, author_id=None, posts=None):
        ids = []
        statusses = {}

        for post in posts:
            ids.append(post.id)
        statusses = dict(super(WallPostDataView, cls).list(post_id__in=ids, author_id=author_id).values_list('post_id', 'is_read'))
        for post in posts:
            post.is_read = statusses.get(post.id, False)
        return posts

    @classmethod
    def add_share_source_to_posts(cls, posts=None, author_id=None):
        ids = []

        for post in posts:
            ids.append(post.id)

        # get all share notifications with relation_1 as post-id and target as this user
        notifications = NotificationDataView.get_share_notification_for_posts_to_user(ids, author_id)
        for post in posts:
            for notification in notifications:
                if post.pk == notification.relation_1:
                    post.share_source = notification.owner
        return posts
        pass
