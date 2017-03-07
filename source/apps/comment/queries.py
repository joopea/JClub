import datetime

from django.db import transaction
from django.db.models import Q
from lib.data_views import DataViewMultipleObjectMixin, DataViewSourceMixin, DataViewSingleObjectMixin


class CommentDataView(DataViewMultipleObjectMixin, DataViewSingleObjectMixin, DataViewSourceMixin):
    app_name = 'comment'
    model = 'Comment'
    manager = 'active'

    @classmethod
    def rate_of_growth(cls, time_span=30):
        a_month_ago = datetime.date.today() - datetime.timedelta(days=time_span)
        total = cls.get_queryset().filter(created__gt=a_month_ago).count()
        return round((1.0 * total) / time_span, 2)

    @classmethod
    def count(cls):
        return cls.get_queryset().count()

    @classmethod
    def by_id(cls, comment_id):
        return cls.get_or_none(id=comment_id)

    @classmethod
    def list(cls, **kwargs):
        return super(CommentDataView, cls).list(**kwargs).select_related('author')

    @classmethod
    def last(cls, post_id):
        return cls.list(post_id=post_id).latest('created')

    @classmethod
    def first_and_last(cls, post_id):
        display_first = 2
        display_last = 2
        comments = cls.list(post_id=post_id)

        total_comments = len(comments)

        remaining = total_comments - (display_first + display_last)

        if remaining <= 0:
            first = comments
            last = []
            remaining = 0
        else:
            first = comments[:display_first]
            last = list(reversed(comments.order_by('-created')[:display_last]))

        return {'first': first, 'last': last, 'remaining': remaining}

    @classmethod
    def post_page(cls, post_id, start_id, end_id, page_size):
        display_first = 2
        display_last = 2
        comments = cls.list(post_id=post_id, id__gt=start_id, id__lt=end_id)

        remaining = max(0, len(comments) - page_size)

        return {'comments': comments[:page_size], 'remaining': remaining}


class CommentSearchView(CommentDataView):
    @classmethod
    def search(cls, query, community_only=True, wall_type=None, wall_id=None, limit=5):
        qs = cls.get_queryset()

        qs = qs.filter(
            Q(message__icontains=query)
        )

        if community_only:
            qs = qs.exclude(post__community__isnull=True)

        if wall_type == 'user':
            qs = qs.filter(post__wall_posts__id=wall_id)
        elif wall_type == 'community':
            qs = qs.filter(post__community_id=wall_id)

        return qs


class AddPostComments(object):
    @classmethod
    def all(cls, post=None):
        post.comments = CommentDataView.list(post=post)

    @classmethod
    def to(cls, posts):
        for post in posts:
            post.first_comments = cls.first_by_post(post=post)
            post.comments = cls.latest_by_post(post=post)

    @classmethod
    def first_by_post(cls, post, limit=3):
        return CommentDataView.list(post=post)[0:limit]

    @classmethod
    def latest_by_post(cls, post, limit=2):
        if post.comment_set.count() <= 3:
            return []

        limit = min(limit, post.comment_set.count() - 3)

        if limit <= 0:
            return []

        return reversed(CommentDataView.list(post=post).order_by('-created')[:limit])


class CommentLikeCount(CommentDataView):
    @classmethod
    def update(cls, comment):
        model = cls.get_model()

        with transaction.atomic():
            comment = model.active.select_for_update().get(id=comment.id)
            model.active.filter(id=comment.id).update(like_count=comment.likecomment_set.count())
