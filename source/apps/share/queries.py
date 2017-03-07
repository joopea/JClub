import datetime
from django.db import connection
from django.db.models import Count, Q
from lib.data_views import ModelDataView, RawQueryMixin
from apps.notifications.models import Notification


class ShareDataView(ModelDataView, RawQueryMixin):
    model = 'Notification'
    app_name = 'notifications'

    @classmethod
    def get_count(cls):
        return cls.list(subject__in=[Notification.SHARE_POST, Notification.FOLLOWEE_SHARE_POST]).count()

    @classmethod
    def growth_by_day(cls, time_span=30):
        a_month_ago = datetime.date.today() - datetime.timedelta(days=time_span)
        return cls\
            .list(Q(created__gt=a_month_ago), subject__in=[Notification.SHARE_POST, Notification.FOLLOWEE_SHARE_POST])\
            .extra({'created': 'date(created)'})\
            .values('created')\
            .annotate(created_count=Count('id'))

    @classmethod
    def get_count_per_community(cls):
        # get all communities with their count
        qs = cls.get_manager().raw(
            """
            SELECT c.*, COUNT(n.id)
            FROM community_community c
            LEFT JOIN post_post p ON p.community_id = c.id
            LEFT JOIN notifications_notification n ON n.relation_1 = p.id
            WHERE n.subject IN('SHARE_POST', 'FOLLOWEE_SHARE_POST')
            GROUP BY c.id
            """
        )
        values = []
        for item in qs:
            values.append(item)
        return values

    @classmethod
    def growth_by_day_per_community(cls, communities, time_span=30):
        results = {}
        for community in communities:
            if connection.vendor == 'postgresql':
                data = cls.raw("""
                    SELECT date_trunc('day', n.created), COUNT(n.id)

                    FROM notifications_notification n
                    LEFT JOIN post_post p ON p.id = n.relation_1
                    LEFT JOIN community_community c ON c.id = p.community_id

                    WHERE n.subject IN('SHARE_POST', 'FOLLOWEE_SHARE_POST')
                    AND n.created > now() - INTERVAL '{time_span} days'
                    AND c.id = {id}

                    GROUP BY date_trunc('day', n.created)

                    """.format(time_span=time_span, id=community.id))
            else:
                data = cls.raw("""
                    SELECT DATE_FORMAT(n.created, '%%Y-%%,-%%d') as date_trunc, COUNT(n.id)

                    FROM notifications_notification n
                    LEFT JOIN post_post p ON p.id = n.relation_1
                    LEFT JOIN community_community c ON c.id = p.community_id

                    WHERE n.subject IN('SHARE_POST', 'FOLLOWEE_SHARE_POST')
                    AND n.created > now() - INTERVAL {time_span} DAY
                    AND c.id = {id}

                    GROUP BY DATE(n.created)

                    """.format(time_span=time_span, id=community.id))
            results[community.name] = data
        return results
