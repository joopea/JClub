from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model

from apps.core.views import ExtraFormDataMixin
from apps.core.exceptions import Json404


class WithGenericForeignKey(ExtraFormDataMixin):

    object_id_field = 'pk'
    object_model_field = 'model'

    def get_object_id(self):
        try:
            return self.kwargs.get(self.object_id_field)
        except KeyError:
            raise Exception('An id is required for objects with a generic foreign key, '
                            'try adding it to the url definition as a pattern-match.')

    def get_content_type(self):
        try:
            model = self.kwargs.get('model')
            if isinstance(model, basestring):
                model = get_model(*model.split('.', 1))
        except KeyError:
            raise Exception('A model is required for objects with a generic foreign key, '
                            'try adding it to the url definition as an argument.')

        if not hasattr(model, '_meta'):
            raise Exception('Model provided should be an object not a string')

        #make sure our relation can exist by checking if our generic foreign key leads somewhere
        if not model.objects.filter(pk=self.get_object_id()).exists():
            raise Json404()

        return ContentType.objects.get_for_model(model).pk

    def get_extra_data(self, *args, **kwargs):
        context = dict()

        context['object_id'] = self.get_object_id()
        context['content_type'] = self.get_content_type()

        return context
