import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F, Count

from apps.post.queries import PostDataView
from apps.community.queries import CommunityDataView
from lib.data_views import DataViewSourceMixin, DataViewMultipleObjectMixin


class HottestCommunityDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'suggestions'
    model = 'HottestCommunity'

    @classmethod
    def get(cls):
        items = super(HottestCommunityDataView, cls).list()
        if len(items):
            item = items[0]
        else:
            item = cls.get_model()(**{
                'like_ratio': 1,
                'share_ratio': 1,
                'comment_ratio': 1,
                'post_ratio': 1,
                'interval': 0,
                'modified': datetime.datetime(1900, 1, 1)
            })

        now = datetime.datetime.now()
        delta = now - item.modified
        if delta.days < item.interval:
            # re-calculate the "Hottest community"
            hottest_communities = CommunityDataView\
                .get_queryset()\
                .annotate(ranking=Sum(
                    F('community_post__like_count') * item.like_ratio +
                    F('community_post__share_count') * item.share_ratio +
                    F('community_post__comment_count') * item.comment_ratio
                ))\
                .order_by('-id')

            hottest_communities_posts = CommunityDataView\
                .get_queryset()\
                .annotate(total=Count('community_post__id'))\
                .order_by('-id')

            for community in hottest_communities:
                for c in hottest_communities_posts:
                    if c.id == community.id:
                        if community.ranking is None:
                            community.ranking = 0
                        community.ranking = community.ranking + c.total * item.post_ratio
                        break

            if len(hottest_communities):
                highest_community = hottest_communities[0]
                for community in hottest_communities:
                    if highest_community.ranking < community.ranking:
                        highest_community = community

                item.community = highest_community
                item.save()
        try:
            return item.community
        except:
            return None


class HottestPostDataView(DataViewMultipleObjectMixin, DataViewSourceMixin):
    app_name = 'suggestions'
    model = 'HottestPost'

    @classmethod
    def get(cls):
        items = super(HottestPostDataView, cls).list()
        if len(items):
            item = items[0]
        else:
            item = cls.get_model()(**{
                'like_ratio': 1,
                'share_ratio': 1,
                'comment_ratio': 1,
                'interval': 0,
                'modified': datetime.datetime(1900, 1, 1)
            })

        now = datetime.datetime.now()
        delta = now - item.modified
        if delta.days > item.interval:
            # re-calculate the "Hottest post"
            new_hottest_post = PostDataView\
                .get_queryset()\
                .extra(select={
                    'ranking':
                        'like_count * %5.2f + share_count * %5.2f + comment_count * %5.2f' %
                        (item.like_ratio, item.share_ratio, item.comment_ratio)
                })\
                .extra(order_by=['-ranking'])
            if len(new_hottest_post):
                item.post = new_hottest_post[0]
                item.save()
            else:
                item = cls.get_model()(**{
                    'like_ratio': 1,
                    'share_ratio': 1,
                    'comment_ratio': 1,
                    'interval': 0,
                    'modified': datetime.datetime(1900, 1, 1)
                })
        try:
            return item.post
        except ObjectDoesNotExist:
            return None


class PromotedPostDataView(DataViewMultipleObjectMixin, DataViewSourceMixin):
    app_name = 'post'
    model = 'Post'
    manager = 'active'

    @classmethod
    def get(cls):
        promoted_posts = super(PromotedPostDataView, cls).\
            list(promotedpost__isnull=False).\
            order_by('-promotedpost__created')
        if len(promoted_posts):
            return promoted_posts[0]


class SuggestionsQuery(object):
    def get(self):
        return {
            'promoted_post': PromotedPostDataView.get(),
            'hottest_post': HottestPostDataView.get(),
            'hottest_community': HottestCommunityDataView.get()
        }
