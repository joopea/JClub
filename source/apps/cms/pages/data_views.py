from lib.data_views import ModelDataView


class PageDataView(ModelDataView):
    model = 'Page'
    app_name = 'pages'

    @classmethod
    def get_pages(cls):
        return cls.list()
