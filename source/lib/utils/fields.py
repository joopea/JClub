# coding: utf-8

# PYTHON IMPORTS
import os
from django import forms
from filebrowser.fields import FileBrowseFormField, FileBrowseField, FileBrowseWidget
from filebrowser.settings import DIRECTORY, MEDIA_ROOT


class CustomFileBrowseFormField(FileBrowseFormField):

    def clean(self, value):
        value = super(FileBrowseFormField, self).clean(value)

        if value == '':
            return value

        # First see whether the path in within the upload directory
        if not value.lower().startswith(DIRECTORY.lower()):
            raise forms.ValidationError("Path: {0} is invalid".format(value))

        # And see if we have access to the path.
        prefix = "/" if not value.startswith('/') else ""
        path = '{0}{1}{2}'.format(MEDIA_ROOT, prefix, value)

        if not os.access(os.path.dirname(path), os.W_OK):
            raise forms.ValidationError("Path: {0} is invalid or cannot be read".format(value))

        return value


class CustomFileBrowseField(FileBrowseField):

    def formfield(self, **kwargs):
        attrs = {}
        attrs["filebrowser_site"] = self.site
        attrs["directory"] = self.directory
        attrs["extensions"] = self.extensions
        attrs["format"] = self.format
        defaults = {
            'form_class': CustomFileBrowseFormField,
            'widget': FileBrowseWidget(attrs=attrs),
            'filebrowser_site': self.site,
            'directory': self.directory,
            'extensions': self.extensions,
            'format': self.format
        }
        return super(FileBrowseField, self).formfield(**defaults)
