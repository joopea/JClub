from django import forms


class ColorPickerWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        html = super(ColorPickerWidget, self).render(name, value, attrs)
        return html

    class Media:
        js = ('widgets/colorpicker/colorwheel.js', )

