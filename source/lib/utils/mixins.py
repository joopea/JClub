from django.template.loader import render_to_string
from django.utils.html import mark_safe


class Renderable(object):
    template_name = None
    mark_safe = False 

    def get_template_name(self):
        if self.template_name is None:
            raise ImproperlyConfigured(
                "Renderable requires either a definition of 'template_name' or "
                "an implementation of 'get_template_name()'"
            )
        else:
            return self.template_name

    def get_context_data(self, **kwargs):
        return kwargs.copy()

    def render(self, context):
        output = render_to_string(
            self.get_template_name(),
            self.get_context_data(context),
        )

        if self.mark_safe:
            output = mark_safe(output)

        return output
