from django.db import connection
from django.db.models import Q
from lib.data_views import DataViewSourceMixin, DataViewMultipleObjectMixin, RawQueryMixin

from apps.follow.queries import FollowCommunityDataView


class CommunityDataView(DataViewSourceMixin, DataViewMultipleObjectMixin, RawQueryMixin):
    app_name = 'community'
    model = 'Community'

    @classmethod
    def number_of_post_likes_per_community(cls):
        return cls.raw("""
            SELECT c.name as community, COUNT(l.id) as total
            FROM community_community c
            LEFT JOIN post_post p ON p.community_id = c.id
            LEFT JOIN like_likepost l ON l.post_id = p.id
            GROUP BY c.name
            """)

    @classmethod
    def number_of_comment_likes_per_community(cls):
        return cls.raw("""
            SELECT c.name as community, COUNT(l.id) as total
            FROM community_community c
            LEFT JOIN post_post p ON p.community_id = c.id
            LEFT JOIN comment_comment cm ON cm.post_id = p.id
            LEFT JOIN like_likepost l ON l.comment_id = cm.id
            GROUP BY c.name
            """)

    @classmethod
    def number_of_comments_per_community(cls):
        data = cls.raw("""
            SELECT c.name as community, COUNT(cm.id) as total
            FROM community_community c
            LEFT JOIN post_post p ON p.community_id = c.id
            LEFT JOIN comment_comment cm ON cm.post_id = p.id
            GROUP BY c.name
            """)
        return data

    @classmethod
    def number_of_posts_per_community(cls):
        data = cls.raw("""
            SELECT c.name as community, COUNT(p.id) as total
            FROM community_community c
            LEFT JOIN post_post p ON p.community_id = c.id
            GROUP BY c.name
            """)
        return data

    @classmethod
    def rate_of_growth_of_comments_per_community(cls, time_span=30):
        result = []
        if connection.vendor == 'postgresql':
            data = cls.raw("""
                SELECT c.name as community, COUNT(cm.id) as total
                FROM community_community c
                LEFT JOIN post_post p ON p.community_id = c.id
                LEFT JOIN comment_comment cm ON cm.post_id = p.id
                WHERE cm.created > now() - INTERVAL '{time_span} days'
                GROUP BY c.name
                """.format(time_span=time_span))
        else:
            data = cls.raw("""
                SELECT c.name as community, COUNT(cm.id) as total
                FROM community_community c
                LEFT JOIN post_post p ON p.community_id = c.id
                LEFT JOIN comment_comment cm ON cm.post_id = p.id
                WHERE cm.created > now() - INTERVAL {time_span} DAY
                GROUP BY c.name
                """.format(time_span=time_span))
        for row in data:
            result.append({
                'community': row['community'],
                'growth_rate': round((1.0 * row['total']) / time_span, 2)
            })
        return result

    @classmethod
    def rate_of_growth_of_posts_per_community(cls, time_span=30):
        result = []
        if connection.vendor == 'postgresql':
            data = cls.raw("""
                SELECT c.name as community, COUNT(p.id) as total
                FROM community_community c
                LEFT JOIN post_post p ON p.community_id = c.id
                WHERE p.created > now() - INTERVAL '{time_span} days'
                GROUP BY c.name
                """.format(time_span=time_span))
        else:
            data = cls.raw("""
                SELECT c.name as community, COUNT(p.id) as total
                FROM community_community c
                LEFT JOIN post_post p ON p.community_id = c.id
                WHERE p.created > now() - INTERVAL {time_span} DAY
                GROUP BY c.name
                """.format(time_span=time_span))
        for row in data:
            result.append({
                'community': row['community'],
                'growth_rate': round((1.0 * row['total']) / time_span, 2)
            })
        return result

    @classmethod
    def growth_rate_followers(cls, time_span=30):
        results = []
        if connection.vendor == 'postgresql':
            data = cls.raw("""
                SELECT c.name as community, COUNT(f.id) as growth

                FROM community_community c
                LEFT JOIN follow_followcommunity f ON f.community_id = c.id

                WHERE f.created > now() - INTERVAL '{time_span} days'

                GROUP BY c.name

                """.format(time_span=time_span))
        else:
            data = cls.raw("""
                SELECT c.name as community, COUNT(f.id) as growth

                FROM community_community c
                LEFT JOIN follow_followcommunity f ON f.community_id = c.id

                WHERE f.created > now() - INTERVAL {time_span} DAY

                GROUP BY c.name

                """.format(time_span=time_span))
        for row in data:
            results.append({
                'community': row['community'],
                'growth_rate': round((1.0 * row['growth']) / time_span, 2)
            })
        return results


class MenuUserCommunityDataView(CommunityDataView):
    app_name = 'community'
    model = 'Community'

    @classmethod
    def list(cls, user_id=None):
        community_ids = list(FollowCommunityDataView.list(user_id=user_id).values_list('community_id', flat=True))
        return CommunityDataView.list(id__in=community_ids)


class CommunitySearchView(CommunityDataView):
    @classmethod
    def search(cls, query, limit=5):
        qs = cls.get_queryset()

        qs = qs.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        return qs[:limit]
