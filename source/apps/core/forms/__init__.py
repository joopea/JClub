from django import forms

# allow import form module
from .constraints import *

# used for export
ValidationError = forms.ValidationError


class ModelForm(forms.ModelForm):
    # augmented ModelForm which copies extra-data to the form data

    def __init__(self, *args, **kwargs):
        if 'data' not in kwargs:
            kwargs['data'] = {}
        kwargs['data'].update(kwargs.pop('extra', {}))
        super(ModelForm, self).__init__(*args, **kwargs)

    def after_save(self, response):
        return response
