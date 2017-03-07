from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from apps.comment.models import Comment
from apps.custom_admin.admin import ImprovedRawIdFields
from apps.notifications.queries import NotificationDataView


class CommentAdmin(ImprovedRawIdFields):
    date_hierarchy = 'created'
    list_display = ['post', 'get_community', 'author', 'created', 'published', 'like_count']
    search_fields = ['post__title', 'post__community__name', 'author__username', 'message']
    list_filter = ['created', 'published']
    raw_id_fields = ['author', 'post']
    fields = ['image', 'author', 'post', 'message']

    def get_community(self, obj):
        return obj.post.community

    get_community.short_description = _('Community')
    get_community.admin_order_field = 'post__community__name'

    def get_queryset(self, request):
        return self.model.all_objects.get_queryset()

    def delete_model(self, request, obj):
        NotificationDataView.delete_comment(request.user, obj.post.author, obj.post.id, message=obj.post.title)
        super(CommentAdmin, self).delete_model(request, obj)


admin.site.register(Comment, CommentAdmin)
