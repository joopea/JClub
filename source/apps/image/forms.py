import os

from django import forms
from django.conf import settings
from django.forms.util import ErrorList

from xorformfields.forms.fields import FileOrURLField

from filer.models import Image


class WithImage(forms.ModelForm):
    image = FileOrURLField(to='file', required=False)

    def clean_image(self):
        data = self.cleaned_data['image']
        if data and data.name and os.path.splitext(data.name)[1].lower() not in settings.FILER_IMAGE_TYPES:
            raise forms.ValidationError('Only jpg, gif and png images are allowed.')
            # if 'image_0' not in self._errors:
            #     self._errors['image_0'] = ErrorList()
            # self._errors['image_0'].append('Only jpg, gif and png images are allowed.')
        return data

    def save(self, *args, **kwargs):
        if self.cleaned_data['image']:
            img = Image()
            img.file = self.cleaned_data['image']
            img.name = img.file.name
            img.save()
            self.instance.image = img
        return super(WithImage, self).save(*args, **kwargs)
