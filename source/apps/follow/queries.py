import datetime
from django.db.models import Count

from lib.data_views import DataViewSourceMixin, DataViewMultipleObjectMixin


class FollowUserDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'follow'
    model = 'FollowUser'

    @classmethod
    def is_followed(cls, author, target):
        return cls.list(author=author, target=target).exists()

    @classmethod
    def followers(cls, followee_id):
        return cls.list(target=followee_id)

    @classmethod
    def is_following(cls, user, target):
        following = getattr(user, '_following_users', None)

        if following is None:
            following = cls.list(author=user).values_list('target_id', flat=True)

            setattr(user, '_following_users', following)

        return target.id in following


class MenuUserFollowUserDataView(FollowUserDataView):
    @classmethod
    def list(cls, user_id=None):
        items = super(MenuUserFollowUserDataView, cls).list(author_id=user_id).prefetch_related('target')
        if items is not None:
            items = items[0:5]
        return items


class FollowCommunityDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'follow'
    model = 'FollowCommunity'

    @classmethod
    def list(cls, user_id=None):
        return super(FollowCommunityDataView, cls).list(author_id=user_id)


class FollowersWallDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'wall'
    model = 'Wall'

    @classmethod
    def list(cls, user_id):
        return super(FollowersWallDataView, cls).list(author__author_followuser__target_id=user_id)


class FollowersCommunityDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'users'
    model = 'User'

    @classmethod
    def list(cls, community_id=None):
        return super(FollowersCommunityDataView, cls).list(author_followcommunity__community_id=community_id)
