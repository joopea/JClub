from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from apps.core.views import AjaxFormResponseMixin

from apps.comment.queries import CommentSearchView
from apps.community.queries import CommunitySearchView
from apps.menu.views import WithUserMenu
from apps.post.queries import PostSearchView


class SearchView(WithUserMenu, TemplateView):
    http_method_names = ['get']

    def get_template_names(self):
        if self.request.is_ajax():
            return 'search/_results.html'

        return 'search/results.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()

        query = self.request.GET.get('q', '')

        context['query'] = query
        context['posts'] = []
        context['comments'] = []
        context['communities'] = []

        if not len(query):
            return context

        community_only = not self.request.user.is_authenticated()

        wall_type = self.request.GET.get('wall_type', None)
        wall_id = self.request.GET.get('wall_id', None)

        # Don't allow searching on a user wall if not logged in
        if wall_type == 'user' and community_only:
            return context

        if wall_type not in ['user', 'community']:
            wall_type = None

        try:
            wall_id = int(wall_id)
        except Exception, e:
            wall_type = None
            wall_id = None

        if self.request.is_ajax():
            limit_posts = limit_comments = limit_communities = 2;
        else:
            limit_posts = 5
            limit_comments = 5
            limit_communities = 2

        context['posts'] = PostSearchView.search(
            query=query,
            limit=limit_posts,
            community_only=community_only,
            wall_type=wall_type,
            wall_id=wall_id,
        )

        context['comments'] = CommentSearchView.search(
            query=query,
            limit=limit_comments,
            community_only=community_only,
            wall_type=wall_type,
            wall_id=wall_id,
        )

        # Don't bother searching for communities on a single wall
        if not wall_type:
            context['communities'] = CommunitySearchView.search(
                query=query,
                limit=limit_communities,
            )

        return context

class SearchOnWall(object):
    def get_context_data(self, **kwargs):
        context = super(SearchOnWall, self).get_context_data(**kwargs)

        context['search_on_wall'] = {
            'wall_type': self.wall_type,
            'wall_id': self.wall_id,
        }

        return context
