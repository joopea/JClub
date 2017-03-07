import datetime

from django.db import transaction
from django.db.models import Q
from lib.data_views import DataViewMultipleObjectMixin, DataViewSourceMixin, DataViewSingleObjectMixin
from apps.notifications.queries import NotificationDataView


class PostDataView(DataViewMultipleObjectMixin, DataViewSingleObjectMixin, DataViewSourceMixin):
    app_name = 'post'
    model = 'Post'
    manager = 'active'

    @classmethod
    def count(cls):
        return cls.get_queryset().count()

    @classmethod
    def rate_of_growth(cls, time_span=30):
        a_month_ago = datetime.date.today() - datetime.timedelta(days=time_span)
        total = cls.get_queryset().filter(created__gt=a_month_ago).count()
        return round((1.0 * total) / time_span, 2)

    @classmethod
    def by_id_or_404(cls, post_id):
        return cls.get_or_404(id=post_id)

    @classmethod
    def by_id(cls, post_id):
        return cls.get_or_none(id=post_id)

    @classmethod
    def list(cls, *args, **kwargs):
        qs = super(PostDataView, cls).list(*args, **kwargs)

        return qs.select_related('author', 'community')


class WallCollection(PostDataView):
    @classmethod
    def list(cls, user_id=None, start=None, limit=None):
        if user_id is None:
            return []

        qs = super(WallCollection, cls).list()

        posts = qs.filter(wall_posts__author_id=user_id).order_by('-wall_posts__created')

        return posts


class WallOwnPostCollection(PostDataView):
    @classmethod
    def list(cls, user_id=None, start=None, limit=None):
        if user_id is None:
            return []

        qs = super(WallOwnPostCollection, cls).list()

        posts = qs\
            .filter(wall_posts__author_id=user_id, wall_posts__post__author_id=user_id)\
            .order_by('-wall_posts__created')
        return posts


class CommunityWallCollection(PostDataView):
    @classmethod
    def list(cls, community_id=None, start=None, limit=None):
        if community_id is None:
            return []

        qs = super(CommunityWallCollection, cls).list()

        return qs.filter(community_id=community_id).order_by('-created')


class PostSearchView(PostDataView):
    @classmethod
    def search(cls, query, community_only=True, wall_type=None, wall_id=None, limit=5):
        if wall_type == 'user':
            qs = WallCollection.list(user_id=wall_id)
        elif wall_type == 'community':
            qs = CommunityWallCollection.list(community_id=wall_id)
        else:
            qs = cls.list()

        qs = qs.filter(
            Q(title__icontains=query) |
            Q(message__icontains=query)
        )

        if community_only:
            qs = qs.exclude(community__isnull=True)

        return qs[:limit]


class PostLikeCount(PostDataView):
    @classmethod
    def update(cls, post):
        if post.published:
            model = cls.get_model()
            with transaction.atomic():
                post = model.active.select_for_update().get(id=post.id)
                model.active.filter(id=post.id).update(like_count=post.post_like.count())


class PostShareCount(PostDataView):
    @classmethod
    def update(cls, post):
        if post.published:
            model = cls.get_model()
            with transaction.atomic():
                post = model.active.select_for_update().get(id=post.id)
                # share count is the number of "SHARE_POST" notifications
                model.active.filter(id=post.id).update(
                    share_count=NotificationDataView.get_share_post_notifications_count(post.id)
                )


class PostCommentCount(PostDataView):
    @classmethod
    def update(cls, post):
        if post.published:
            model = cls.get_model()
            with transaction.atomic():
                post = model.active.select_for_update().get(id=post.id)
                model.active.filter(id=post.id).update(comment_count=post.comment_set.count())
