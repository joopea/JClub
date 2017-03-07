from lib.data_views import DataViewSourceMixin, DataViewMultipleObjectMixin


class SaveDataView(DataViewSourceMixin, DataViewMultipleObjectMixin):
    app_name = 'save'
    model = 'Save'


class SavedByUserDataView(SaveDataView):
    @classmethod
    def is_saved(cls, user, post):
        saved = getattr(user, '_saved_posts', None)

        if saved is None:
            saved = cls.list(author_id=user).values_list('post_id', flat=True)

            setattr(user, '_saved_posts', saved)

        return post.id in saved