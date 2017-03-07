from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.core.forms import WithAuthor

from .models import Report


class ReportForm(WithAuthor, forms.ModelForm):
    class Meta:
        model = Report
        fields = (
            'message',
        )
        labels = {
            'message': _('Why do you want to report this post?')
        }


class AdminReportForm(ReportForm):

    def clean(self):
        post = self.cleaned_data.get('post')
        comment = self.cleaned_data.get('comment')

        if post and comment:
            raise forms.ValidationError("Both Post and Comment are not permitted")

        if not post and not comment:
            raise forms.ValidationError("Provide either a post or comment to report about")

    class Meta:
        model = Report
        fields = ['message', 'post', 'comment', 'author']
        labels = {
            'message': _('Why do you want to report this comment/ post?')
        }
