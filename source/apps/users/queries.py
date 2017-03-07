import datetime
from django.db.models import Count, Q
from lib.data_views import ModelDataView, RecordDoesNotExist, DataViewSourceMixin, DataViewMultipleObjectMixin, \
    RawQueryMixin
from lib.users.data_views import UserDataView as BaseUserDataView

from apps.follow.queries import MenuUserFollowUserDataView
from apps.notifications.queries import NotificationDataView
from apps.community.queries import MenuUserCommunityDataView


class UserDataView(BaseUserDataView, RawQueryMixin):

    @classmethod
    def alert_count(cls, alert_count=3):
        return cls.get_queryset().raw("""
            SELECT u.id, u.username, COUNT(n.id) as total
            FROM users_user u
            LEFT JOIN notifications_notification n ON n.owner_id = u.id
            WHERE n.subject IN({warning_types})
            AND u.is_active IS True
            GROUP BY u.id, u.username
            HAVING COUNT(n.id) >= {alert_count}
            ORDER BY total DESC
            """.format(
                warning_types="'"+"','".join(NotificationDataView.get_warning_types())+"'",
                alert_count=alert_count))

    @classmethod
    def by_username(cls, username):
        kwargs = {
            cls.get_model().USERNAME_FIELD: username
        }

        try:
            return cls.get(**kwargs)
        except RecordDoesNotExist:
            return None

    @classmethod
    def delete(cls, user):
        # if fails, then do exception
        cls.get(id=user.id).delete()

    @classmethod
    def from_list(cls, ids):
        return cls.list(id__in=ids)

    @classmethod
    def get_active_user_count(cls):
        return cls.list(is_active=True).count()

    @classmethod
    def get_active_users_by_day(cls, time_span=30):
        a_month_ago = datetime.date.today() - datetime.timedelta(days=time_span)
        return cls\
            .list(Q(date_joined__gt=a_month_ago), is_active=True)\
            .extra({'date_joined': 'date(date_joined)'})\
            .values('date_joined')\
            .annotate(created_count=Count('id'))


class UserProfile(object):
    @staticmethod
    def get(user_id=None):
        return {
            'user': UserDataView.get_or_none(pk=user_id),
            'notifications': NotificationDataView.by_user(user_id=user_id),
            'new_notifications': NotificationDataView.get_unread_notifications_count(user_id=user_id),
            'communities': list(MenuUserCommunityDataView.list(user_id=user_id)),
            'following': list(MenuUserFollowUserDataView.list(user_id=user_id))
        }


class UsernameVariationDataView(ModelDataView):
    model = 'UsernameVariation'
    app_name = 'users'

    @classmethod
    def generate(cls, username):

        if cls.list(username=username).exists():
            return False

        variations = []
        username_variant = cls.get_model()

        for i in range(1000):
            variations.append(
                username_variant(
                    username_id=username.id,
                    username_variation=u'{0}{1}'.format(unicode(username.username), unicode(i)),
                    username_variation_no=i,
                )
            )

        cls.get_manager().bulk_create(variations)

        return True

    @classmethod
    def empty_list(cls):
        return cls.get_queryset().none()

    @classmethod
    def by_username(cls, username_id, limit=100):
        try:
            return cls.list(username_id=username_id)
        except ValueError:
            return []

    @classmethod
    def remove(cls, username_variation_id):
        cls.get(id=username_variation_id).delete()


class UsernameDataView(ModelDataView):
    model = 'Username'
    app_name = 'users'

    @classmethod
    def active(cls):
        return cls.list(active=True)


class SecurityQuestionDataView(ModelDataView):
    model = 'SecurityQuestion'
    app_name = 'users'

    @classmethod
    def all(cls):
        return cls.list()


class FollowingUserDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'follow'
    model = 'FollowUser'

    @classmethod
    def list(cls, user=None):
        followers = super(FollowingUserDataView, cls).list(author=user).values_list('target', flat=True)
        return UserDataView.from_list(followers)


class FollowedUserDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'follow'
    model = 'FollowUser'

    @classmethod
    def list(cls, user=None):
        followed = super(FollowedUserDataView, cls).list(target=user).values_list('author', flat=True)
        return UserDataView.from_list(followed)