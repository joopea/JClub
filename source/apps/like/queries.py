import datetime
from django.db import connection
from django.db.models import Count, Q

from lib.data_views import DataViewSourceMixin, DataViewMultipleObjectMixin, RawQueryMixin


class LikePostDataView(DataViewSourceMixin, DataViewMultipleObjectMixin, RawQueryMixin):
    app_name = 'like'
    model = 'LikePost'

    @classmethod
    def rate_of_growth_per_community(cls, time_span=30):
        if connection.vendor == 'postgresql':
            data = cls.raw("""
                SELECT c.name, COUNT(l.id) as total
                FROM like_likepost l
                LEFT JOIN post_post p ON l.post_id = p.id
                LEFT JOIN community_community c ON p.community_id = c.id
                WHERE l.created > now() - INTERVAL '{time_span} days'
                GROUP BY c.name
                """.format(time_span=time_span))
        else:
            data = cls.raw("""
                SELECT c.name, COUNT(l.id) as total
                FROM like_likepost l
                LEFT JOIN post_post p ON l.post_id = p.id
                LEFT JOIN community_community c ON p.community_id = c.id
                WHERE l.created > now() - INTERVAL {time_span} DAY
                GROUP BY c.name
                """.format(time_span=time_span))
        for row in data:
            row['growth_rate'] = round((1.0 * row['total']) / time_span, 2)
        return data

    @classmethod
    def growth_by_day(cls, time_span=30):
        if connection.vendor == 'postgresql':
            return cls.raw("""
                SELECT date_trunc('day', l.created), COUNT(l.id)
                FROM like_likepost l
                WHERE l.created > now() - INTERVAL '{time_span} days'
                GROUP BY date_trunc('day', l.created)
                """.format(time_span=time_span))
        return cls.raw("""
            SELECT DATE_FORMAT(l.created, '%%Y-%%m-%%d') as date_trunc, COUNT(l.id)
            FROM like_likepost l
            WHERE l.created > now() - INTERVAL {time_span} DAY
            GROUP BY DATE(l.created)
            """.format(time_span=time_span))

    @classmethod
    def count_per_community(cls):
        return cls.raw("""
            SELECT c.name, COUNT(l.id) as total
            FROM like_likepost l
            LEFT JOIN post_post p ON p.id = l.post_id
            LEFT JOIN community_community c ON p.community_id = c.id
            GROUP BY c.name
            """)

    @classmethod
    def rate_of_growth_by_day(cls, time_span=30):
        a_month_ago = datetime.date.today() - datetime.timedelta(days=time_span)
        return cls\
            .list(Q(created__gt=a_month_ago), is_active=True)\
            .extra({'created': 'date(created)'})\
            .values('created')\
            .annotate(created_count=Count('id'))

    @classmethod
    def rate_of_growth(cls, time_span=30):
        a_month_ago = datetime.date.today() - datetime.timedelta(days=time_span)
        total = cls.get_queryset().filter(created__gt=a_month_ago).count()
        return round((1.0 * total) / time_span, 2)

    @classmethod
    def count(cls):
        return cls.get_queryset().count()

    @classmethod
    def is_liked(cls, user, post):
        liked = getattr(user, '_liked_posts', None)

        if liked is None:
            liked = cls.list(author_id=user).values_list('post_id', flat=True)

            setattr(user, '_liked_posts', liked)

        return post.id in liked


class LikeCommentDataView(DataViewSourceMixin, DataViewMultipleObjectMixin, RawQueryMixin):
    app_name = 'like'
    model = 'LikeComment'

    @classmethod
    def rate_of_growth_per_community(cls, time_span=30):
        if connection.vendor == 'postgresql':
            data = cls.raw("""
                SELECT c.name, COUNT(l.id) as total
                FROM like_likecomment l
                LEFT JOIN comment_comment cm ON l.comment_id = cm.id
                LEFT JOIN post_post p ON cm.post_id = p.id
                LEFT JOIN community_community c ON p.community_id = c.id
                WHERE l.created > now() - INTERVAL '{time_span} days'
                GROUP BY c.name
                """.format(time_span=time_span))
        else:
            data = cls.raw("""
                SELECT c.name, COUNT(l.id) as total
                FROM like_likecomment l
                LEFT JOIN comment_comment cm ON l.comment_id = cm.id
                LEFT JOIN post_post p ON cm.post_id = p.id
                LEFT JOIN community_community c ON p.community_id = c.id
                WHERE l.created > now() - INTERVAL {time_span} DAY
                GROUP BY c.name
                """.format(time_span=time_span))
        for row in data:
            row['growth_rate'] = round((1.0 * row['total']) / time_span, 2)
        return data

    @classmethod
    def growth_by_day(cls, time_span=30):
        if connection.vendor == 'postgresql':
            return cls.raw("""
                SELECT date_trunc('day', l.created), COUNT(l.id)
                FROM like_likecomment l
                WHERE l.created > now() - INTERVAL '{time_span} days'
                GROUP BY 1
                """.format(time_span=time_span))
        return cls.raw("""
            SELECT DATE_FORMAT(l.created, '%%Y-%%m-%%d') as date_trunc, COUNT(l.id)
            FROM like_likecomment l
            WHERE l.created > now() - INTERVAL {time_span} DAY
            GROUP BY DATE(l.created)
            """.format(time_span=time_span))

    @classmethod
    def count_per_community(cls):
        return cls.raw("""
            SELECT c.name, COUNT(l.id) as total
            FROM like_likecomment l
            LEFT JOIN comment_comment cm ON l.comment_id = cm.id
            LEFT JOIN post_post p ON cm.post_id = p.id
            LEFT JOIN community_community c ON p.community_id = c.id
            GROUP BY c.name
            """)

    @classmethod
    def rate_of_growth(cls, time_span=30):
        a_month_ago = datetime.date.today() - datetime.timedelta(days=time_span)
        total = cls.get_queryset().filter(created__gt=a_month_ago).count()
        return round((1.0 * total) / time_span, 2)

    @classmethod
    def count(cls):
        return cls.get_queryset().count()

    @classmethod
    def is_liked(cls, user, comment):
        liked = getattr(user, '_liked_comments', None)

        if liked is None:
            liked = cls.list(author_id=user).values_list('comment_id', flat=True)

            setattr(user, '_liked_comments', liked)

        return comment.id in liked
