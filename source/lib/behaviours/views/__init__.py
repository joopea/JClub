from apps.core.views import ExtraFormDataMixin


class WithAuthor(ExtraFormDataMixin):
    def get_extra_data(self, *args, **kwargs):
        context = super(WithAuthor, self).get_extra_data(*args, **kwargs)
        context['author'] = self.request.user.id
        return context
