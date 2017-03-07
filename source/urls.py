from django.conf import settings
from django.conf.urls import url, patterns, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from throttle.decorators import throttle


urlpatterns = patterns('')

if settings.INSTANCE_TYPE == 'www' or not settings.CHECK_DOMAIN_SEPERATION:
    from apps.core.views import RedirectToDefaultLanguage, HomeView

    handler404 = 'apps.core.views.handle_404'
    handler500 = 'apps.core.views.handle_500'

    urlpatterns += patterns(
        '',
        url(r'^$', RedirectToDefaultLanguage.as_view(permanent=False), name='redirect_to_default_language'),
        url(r'^ckeditor/', include('ckeditor.urls')),
    )

    urlpatterns += i18n_patterns(
        '',
        url(r'^$', HomeView.as_view(), name='home'),
        url(r'^wall/', include('apps.wall.urls', namespace='wall')),
        url(r'^post/', include('apps.post.urls', namespace='post')),

        url(r'', include('apps.block.urls', namespace='block')),
        url(r'', include('apps.comment.urls', namespace='comment')),
        url(r'', include('apps.follow.urls', namespace='follow')),
        url(r'', include('apps.like.urls', namespace='like')),
        url(r'', include('apps.save.urls', namespace='save')),
        url(r'', include('apps.share.urls', namespace='share')),
        url(r'', include('apps.suggestions.urls', namespace='suggestions')),
        url(r'', include('apps.community.urls', namespace='community')),
        url(r'', include('apps.notifications.urls', namespace='notifications')),
        url(r'', include('apps.report.urls', namespace='report')),

        url(r'^account/', include('apps.users.urls', namespace='users')),
        url(r'^search/', include('apps.search.urls', namespace='search')),
        url(r'^menu/', include('apps.menu.urls', namespace='menu')),

        # NOTE!! this should be last, as it matches every "single" url path part (r'^(?P<slug>[-\w]+)/$')
        url(r'', include('apps.cms.pages.urls', namespace='pages')),

    )

if settings.INSTANCE_TYPE == 'admin' or not settings.CHECK_DOMAIN_SEPERATION:
    admin.autodiscover()
    
    login_func = admin.site.login
    
    # Fugly workaround for django-throttle-request:
    # admin.site.login = throttle(admin.site.login) doesn't work, because
    # throttle adds an attribute to the passed view_func, which in this case
    # is an instancemethod of admin.site. This results in an error
    @throttle(zone='admin-login')
    def throttled_login(*args, **kwargs):
        return login_func(*args, **kwargs)
    
    admin.site.login = throttled_login
    admin.site.site_header = 'JoopeA'
    admin.site.site_title = 'JoopeA'
    admin.site.index_title = 'Site administration'

    urlpatterns += patterns(
        '',
        url(r'^admin/report/', include('apps.report.admin_urls', namespace="admin_reports")),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^ckeditor/', include('ckeditor.urls')),
    )

if settings.INSTANCE_TYPE == 'shorturl':
    urlpatterns = patterns(
        '',
        url(r'', include('apps.shorturl.urls', namespace='shorturl'), name='redirect_to_default_language'),
    )

if settings.INSTANCE_TYPE in ('www', 'admin') and settings.DEBUG:
    from apps.core.views import DebugView

    urlpatterns += patterns(
        '',
        url(
            r"^media/(?P<path>.*)$", "django.views.static.serve",
            {"document_root": settings.MEDIA_ROOT,
             "show_indexes": True}
        ),
        url(
            r"^static/(?P<path>.*)$", "django.views.static.serve",
            {"document_root": settings.STATIC_ROOT,
             "show_indexes": True}
        ),
        url(
            r'^csrf_token', DebugView.as_view()
        )
    )
    urlpatterns += staticfiles_urlpatterns()


handler404 = 'apps.core.views.handle_404'
handler500 = 'apps.core.views.handle_500'
