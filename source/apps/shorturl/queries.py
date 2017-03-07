from lib.data_views import ModelDataView


class ShortURLDataView(ModelDataView):
    model = 'ShortURL'
    app_name = 'shorturl'

    @classmethod
    def get_or_create(cls, **kwargs):
        obj, created = cls.get_queryset().get_or_create(**kwargs)
        return obj
