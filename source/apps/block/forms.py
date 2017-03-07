from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS
from apps.block.models import BlockByUser
from apps.core import forms


# class NotBlockedByCommunity(forms.ModelForm):
#     def clean(self):
#         cleaned_data = super(NotBlockedByCommunity, self).clean()
#         author = cleaned_data['author']
#         object = self.get_object(cleaned_data)
#         if BlockByCommunity.objects().filter(target=author.pk, community=object.community).exists():
#             raise forms.ValidationError(
#                 _('You are blocked by the community this item belogs to'),
#                 code='blocked-by-community'
#             )
#         return cleaned_data


class BlockUserForm(forms.ModelForm):
    class Meta:
        model = BlockByUser
        exclude = []
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _("You've already blocked this user!")
            }
        }
