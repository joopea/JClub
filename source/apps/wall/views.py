from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from apps.users.queries import UserDataView

from lib.behaviours.views.formview import WithGenericForeignKey
from apps.core.views import ModelFormView, AjaxFormResponseMixin
from lib.behaviours.views import WithAuthor

from apps.comment.queries import AddPostComments
from apps.suggestions.queries import SuggestionsQuery
from apps.menu.views import WithUserMenu
from apps.community.queries import CommunityDataView
from apps.post.queries import PostDataView, WallCollection, CommunityWallCollection, WallOwnPostCollection
from apps.search.views import SearchOnWall

from .models import Wall
from .forms import WallForm
from .queries import WallPostDataView


class SearchOnUserWall(SearchOnWall):
    wall_type = 'user'

    @property
    def wall_id(self):
        return self.user_id


class SearchOnCommunityWall(SearchOnWall):
    wall_type = 'community'

    @property
    def wall_id(self):
        return self.kwargs.get('pk', 0)


class WallListView(ListView):
    def paginate_queryset(self, queryset, page_size):
        paginated = super(WallListView, self).paginate_queryset(queryset, page_size)

        page = paginated[1]

        AddPostComments.to(page.object_list)

        return paginated


class WallList(WithUserMenu, SearchOnUserWall, WallListView):
    template_name = 'wall/wall.html'
    queryset = WallCollection
    paginate_by = 5

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WallList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        self.user_id = self.kwargs.get('pk', self.request.user.pk)
        if self.request.user.username == 'deleted':
            raise Http404
        return self.queryset.list(user_id=self.user_id)

    def get_context_data(self, **kwargs):
        context = super(WallList, self).get_context_data(**kwargs)
        own_wall = (int(self.user_id) == self.request.user.id)
        if not own_wall:
            target_user = UserDataView.by_id(user_id=self.user_id)
        else:
            target_user = self.request.user
            WallPostDataView.add_readstatus_to_posts(posts=context['object_list'], author_id=self.user_id)

        context.update({
            'suggestions': SuggestionsQuery().get(),
            'target_user': target_user,
            'own_wall': own_wall,
            'wall': target_user,
        })

        # if on own wall, the sharing person should be added to the post
        # so you can see the reason this post is on your wall
        if own_wall:
            WallPostDataView.add_share_source_to_posts(posts=context['object_list'], author_id=self.user_id)

        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ['wall/_wall.html']

        return [self.template_name]


class WallOwnPostsList(WithUserMenu, SearchOnCommunityWall, WallListView):
    template_name = 'wall/own.html'
    queryset = WallOwnPostCollection
    paginate_by = 5

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WallOwnPostsList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        self.user_id = self.kwargs.get('pk', self.request.user.pk)
        if self.request.user.username == 'deleted':
            raise Http404
        return self.queryset.list(user_id=self.user_id)

    def get_context_data(self, *args, **kwargs):
        context = super(WallOwnPostsList, self).get_context_data(**kwargs)
        context.update({
            'suggestions': SuggestionsQuery().get(),
            'target_user': self.request.user,
            'own_wall': True,
            'wall': self.request.user,
        })

        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ['wall/_wall.html']
        return [self.template_name]


class CommunityWallList(WithUserMenu, SearchOnCommunityWall, WallListView):
    template_name = 'wall/community_wall.html'
    queryset = CommunityWallCollection
    paginate_by = 5

    def get_queryset(self):
        return self.queryset.list(community_id=self.kwargs.get('pk', 0))

    def get_context_data(self, **kwargs):
        context = super(CommunityWallList, self).get_context_data(**kwargs)
        community = CommunityDataView.list(pk=self.kwargs.get('pk', 0))[:1]
        if len(community):
            context['community'] = community[0]
        else:
            raise Http404
        for community in context['profile']['communities']:
            if community.id == context['community'].id:
                context['community'].following = True
        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ['wall/_wall.html']

        return [self.template_name]


class AjaxMarkWallPostAsRead(CreateView):
    http_method_names = ['post']

    def get_object(self, queryset=None):
        return WallPostDataView.get(user_id=self.request.user.pk, post_id=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        object.is_read = True
        object.save()
        return JsonResponse({'success': True})


class WallDetail(DetailView):
    template_name = 'core/dump.html'
    model = Wall


class WallDelete(WithAuthor, ModelFormView, DeleteView):
    template_name = 'core/dump.html'
    form_class = WallForm
    success_url = 'wall:list'


class WallCreate(WithAuthor, WithGenericForeignKey, ModelFormView, CreateView):
    http_method_names = ['post']
    template_name = 'core/dump.html'
    form_class = WallForm
