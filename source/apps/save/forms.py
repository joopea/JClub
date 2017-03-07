from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS

from apps.core import forms

from .models import Save

#core ModelForm first, Constraints second, actions last
class SaveForm(forms.ModelForm):

    class Meta:
        model = Save
        exclude = []
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _("You've already saved this post!")
            }
        }
