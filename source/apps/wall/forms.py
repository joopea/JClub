from django.db import IntegrityError

from apps.core import forms

from .models import Wall


class WallForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        """
        The business rules allow for attempting to add the same post to a user's wall multiple times
        this is not an error, the desired behaviour is that this will be ignored
        """
        try:
            super(WallForm, self).save(*args, **kwargs)
        except IntegrityError:
            pass

    class Meta:
        model = Wall
        exclude = []
