from lib.data_views import DataViewSourceMixin, DataViewMultipleObjectMixin

from apps.follow.queries import FollowCommunityDataView


class BlockedBy(DataViewSourceMixin, DataViewMultipleObjectMixin):
    @classmethod
    def _is_blocked(cls, user, blocker):
        blocked = getattr(user, cls.cache_key, None)

        if blocked is None:
            blocked = cls.list(target=user).values_list(cls.key, flat=True)

            setattr(user, cls.cache_key, blocked)

        return blocker.id in blocked


class BlockByUserDataView(BlockedBy):
    app_name = 'block'
    model = 'BlockByUser'
    key = 'author_id'
    cache_key = '_blocked_by_users'

    @classmethod
    def is_blocked(cls, user, author): # user blocked by author
        return cls._is_blocked(user, author)


class BlockByCommunityDataView(BlockedBy):
    app_name = 'block'
    model = 'BlockByCommunity'
    key = 'community_id'
    cache_key = '_blocked_by_communities'

    @classmethod
    def is_blocked(cls, user, community):# user blocked by community
        return cls._is_blocked(user, community)


class CommunityDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'community'
    model = 'Community'


class MenuUserCommunityDataView(CommunityDataView):
    app_name = 'community'
    model = 'Community'

    @classmethod
    def list(cls, user_id=None):
        community_ids = list(FollowCommunityDataView.list(user_id=user_id).values_list('community_id', flat=True)[0:5])
        return CommunityDataView.list(id__in=community_ids)


class BlockedUsersDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'users'
    model = 'User'

    @classmethod
    def list(cls, user=None):
        return super(BlockedUsersDataView, cls).list(target_blockbyuser__author=user)
