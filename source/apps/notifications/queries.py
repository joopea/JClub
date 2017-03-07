from lib.data_views import ModelDataView, DataViewConfigError


class NotificationDataView(ModelDataView):
    app_name = 'notifications'
    model = 'Notification'

    @classmethod
    def has_shared(cls, author=None, post=None):
        return cls.get_queryset().filter(author_id=author, relation_1=post, subject=cls.get_model().SHARE_POST).exists()

    @classmethod
    def get_warning_types(cls):
        return cls.get_model().WARNING_TYPES

    @classmethod
    def get_notifications(cls, user_id):
        return cls.get_queryset().filter(owner_id=user_id)

    @classmethod
    def get_notifications_count(cls, user_id):
        return cls.get_notifications(user_id).count()

    @classmethod
    def get_share_notification_for_posts_to_user(cls, post_ids, user_id):
        return cls.get_queryset().filter(
            relation_1__in=post_ids,
            owner_id=user_id,
            subject=cls.get_model().SHARE_POST
        )

    @classmethod
    def get_share_post_notifications_count(cls, post_id):
        return cls.get_queryset().filter(
            relation_1=post_id,
            subject=cls.get_model().SHARE_POST
        ).count()

    @classmethod
    def get_unread_notifications_count(cls, user_id=None):
        return cls.get_notifications(user_id).filter(read=False).count()

    @classmethod
    def by_user(cls, user_id, limit=5):
        return {
            'count': cls.get_notifications_count(user_id),
            'items': list(cls.list(owner_id=user_id)[:limit])
        }

    @classmethod
    def create_share_post_notification(cls, author=None, target=None, post_id=None):
        cls.add(
            author=author,
            owner=target,
            relation_1=post_id,
            subject=cls.get_model().SHARE_POST
        )

    @classmethod
    def create_for_post(cls, followers, notification_type, creator_id, post):

        model = cls.get_model()

        if notification_type not in model.POST_NOTIFICATIONS:
            raise DataViewConfigError("Notification_type must be type of POST_NOTIFICATIONS")

        notifications = []
        for follower in followers:
            notifications.append(model(
                subject=notification_type,
                owner=follower,
                author_id=creator_id,
                relation_1=post.pk
            ))

        cls.get_manager().bulk_create(notifications)

    @classmethod
    def create_post_on_user_wall_notification(cls, author, target_id, post_id):
        model = cls.get_model()
        return cls.get_manager().create(
            author=author,
            owner_id=target_id,
            relation_1=post_id,
            subject=model.SHARE_POST
        )

    @classmethod
    def approval_notification(cls, moderator, target, subject, message='', relation_id=None, to_self=True):
        return cls.add(
            author=moderator,
            owner=target,
            relation_1=relation_id or -1,
            subject=subject,
            to_self=to_self,
            message=message
        )

    @classmethod
    def delete_post(cls, moderator, target, message):
        return cls.add(
            author=moderator,
            owner=target,
            relation_1=-1,
            subject=cls.get_model().DELETED_POST,
            to_self=True,
            message=message
        )

    @classmethod
    def delete_comment(cls, moderator, target, relation, message):
        return cls.add(
            author=moderator,
            owner=target,
            relation_1=relation,
            subject=cls.get_model().DELETED_COMMENT,
            to_self=True,
            message=message
        )

    @classmethod
    def get_alert_count(cls, user):
        return cls.list(owner=user, subject__in=cls.get_model().WARNING_TYPES).count()

    @classmethod
    def get_disapproved_report_subject(cls, obj):
        if obj.is_post:
            return cls.get_model().DISAPPROVED_REPORTED_POST
        if obj.is_comment:
            return cls.get_model().DISAPPROVED_REPORTED_COMMENT

    @classmethod
    def get_approved_report_subject(cls, obj):
        if obj.is_post:
            return cls.get_model().APPROVED_REPORTED_POST
        if obj.is_comment:
            return cls.get_model().APPROVED_REPORTED_COMMENT

    @classmethod
    def add(cls, author, owner, relation_1, subject, message='', to_self=False):

        if author == owner and not to_self:
            return

        cls.get_manager().create(
            author=author,
            owner=owner,
            relation_1=relation_1,
            subject=subject,
            original=message
        )
