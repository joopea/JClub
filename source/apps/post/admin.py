from django.contrib import admin
from apps.custom_admin.admin import ImprovedRawIdFields
from apps.notifications.queries import NotificationDataView
from apps.post.models import Post


class PostAdmin(ImprovedRawIdFields):
    date_hierarchy = 'created'
    list_display = ['title', 'community', 'author', 'created', 'published', 'share_count', 'like_count', 'comment_count']
    search_fields = ['title', 'community__name', 'author__username', 'message']
    list_filter = ['created', 'published']
    raw_id_fields = ['author', 'community']
    fields = ['title', 'image', 'author', 'community', 'message']

    def get_queryset(self, request):
        return self.model.all_objects.get_queryset()

    def delete_model(self, request, obj):
        NotificationDataView.delete_post(request.user, obj.author, message=obj.title)
        super(PostAdmin, self).delete_model(request, obj)


admin.site.register(Post, PostAdmin)
