from functools import update_wrapper
from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth import load_backend, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from lib.utils.functions import switch_language_url


class AsSULoginMixin(object):
    """
    Admin site mixin for logging in as a given user.

    Usage: Add the mixin to your user admin view
    """

    def login_action(self, request, user_id):
        """ Login as given user. """

        user = get_object_or_404(self.model, pk=user_id)

        if not hasattr(user, 'backend'):
            for backend in settings.AUTHENTICATION_BACKENDS:
                if user == load_backend(backend).get_user(user.pk):
                    user.backend = backend
                    break

        login(request, user)

        return HttpResponseRedirect(user.get_absolute_url())

    def login_show(self, obj):
        info = self.get_info()
        return u'<a href="%s">%s</a>' % (reverse('admin:%s_%s_login' % info, kwargs={'user_id': obj.pk}), _('Inloggen'))

    def get_urls(self):
        ret = super(AsSULoginMixin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.get_info()

        urlpatterns = patterns(
            '',
            url(r'^login/(?P<user_id>\d+)/$',
                wrap(self.login_action),
                name='%s_%s_login' % info),
        )

        return urlpatterns + ret

    def get_info(self):
        return self.model._meta.app_label, self.model._meta.model_name


    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        return self.list_display + ("login_show", )

    login_show.allow_tags = True
    login_show.short_description = _("login")


class NextURLMixin(object):
    """
    Mixin for Django FormView, with a wrapper to get the 'next' url param after, for expample, logging in
    """
    next_param = 'next'
    default_redirect_param = '/'
    allow_logged_in = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and not self.allow_logged_in:
            return HttpResponseRedirect(self.get_next_url())
        return super(NextURLMixin, self).dispatch(request, *args, **kwargs)

    def get_next_url(self):
        return self.request.GET.get(self.next_param, self.default_redirect_param)

    def get_success_url(self):
        return self.get_next_url()


class LanguageRedirectMixin(NextURLMixin):
    """
    Mixin with support for language switching after, for example, logging in
    """
    language = settings.LANGUAGE_CODE

    def get_next_url(self):
        next_url = super(LanguageRedirectMixin, self).get_next_url()
        return switch_language_url(self.get_language(), next_url)

    def get_language(self):
        return self.language


class AuthenticationMixin(object):
    login_url = settings.LOGIN_URL

    @method_decorator(login_required(login_url=login_url))
    def dispatch(self, *args, **kwargs):
        return super(AuthenticationMixin, self).dispatch(*args, **kwargs)