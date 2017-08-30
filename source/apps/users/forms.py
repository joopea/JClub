from django import forms
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from form_utils.forms import BetterForm
from apps.users.queries import UserDataView, UsernameDataView, SecurityQuestionDataView, UsernameVariationDataView, UsernameDataView, SecurityQuestionDataView, \
    UserDataView
from apps.users.models import Username
from apps.language.models import Language

from lib.users.forms import BaseLoginForm, BaseUserCreationForm, SetPasswordForm as BaseSetPasswordForm


class LoginForm(BetterForm, BaseLoginForm):
    """
    Default login form
    """

    class Meta:
        fieldsets = [
            ('main', {
                'fields': ['username', 'password'],
                'legend': '',
                'description': ''
            }),
        ]


class UserRegistrationForm(BaseUserCreationForm):
    """
    This form uses a pre-defined list of usernames from which the user has to select one himself.
    username_postfix is depend on the selected username. This field is being updated using javascript,
    initially an empty list is passed. After post the list is updated with the available choices, so
    we have both client and server side validation. The code in __init__ somewhat sucks, but that's the
    only way to set the choices dynamically.

    The form also enables the user to select 2 secret questions for password restore.

    Further the basic Registration form is used.

    Use-cases:

        als de admin een nieuwe username aanmaakt dna worden alle mogelijke combinaties gegenereerd
        dit zodat je bij het maken van het user account een suggestie kunt doen voor een nog mogeiljke combinatie van username+id
        ook kun je zo gemakkelijker valideren of een username nog kan bestaan

        een user bij het aanmelden kan een van die combinaties kiezen.

        een user kiest bij het aanmelden 2 vna die vragen, deze worden gekopieerd naar die user's record

        de secret awnsers op deze questions kunnen persoonlijke data bevatten, en worden daarom met een
        destructief hashing algorithme opgeslagen
    """
    send_mail = False

    username = forms.ModelChoiceField(label=_('username'), empty_label=_("Select a username"), queryset=UsernameDataView.active())
    username_postfix = forms.ModelChoiceField(label=_('username postfix'), queryset=UsernameVariationDataView.empty_list())

    security_question_1 = forms.ModelChoiceField(label=_('Security question 1'), queryset=SecurityQuestionDataView.all())
    security_question_2 = forms.ModelChoiceField(label=_('Security question 2'), queryset=SecurityQuestionDataView.all())

    security_answer_1 = forms.CharField(label=_('Security answer 1'), max_length=255)
    security_answer_2 = forms.CharField(label=_('Security answer 2'), max_length=255)

    language = forms.ModelChoiceField(label=_('Language'), queryset=Language.objects.filter(status='act'))

    privacy_policy = forms.BooleanField(label=_('Privacy policy'))
    terms_of_use = forms.BooleanField(label=_('Terms of use'))

    def __init__(self, *args, **kwargs):

        data = kwargs.get('data')
        if data:
            try:
                username_id = int(data.get('username'))
                self.base_fields['username_postfix'].queryset = UsernameVariationDataView.by_username(username_id)
                self.base_fields['username_postfix'].empty_label = None
            except (ValueError, TypeError):
                pass  # do nothing

        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)

        user.username = self.get_username()
        UsernameVariationDataView.remove(self.cleaned_data.get('username_postfix').id)

        user.language = self.get_language()

        user.profile_colour = self.cleaned_data.get('profile_colour')

        user.security_question_1 = self.cleaned_data.get('security_question_1').question
        user.security_answer_1 = make_password(self.cleaned_data.get('security_answer_1'))
        user.security_question_2 = self.cleaned_data.get('security_question_2').question
        user.security_answer_2 = make_password(self.cleaned_data.get('security_answer_2'))

        user.save()

        return user

    def get_username(self):
        class obj_username_variation(object):
            username_variation_no = 1
        return '{0}-{1}'.format(self.cleaned_data.get('username'), self.cleaned_data.get('username_postfix', obj_username_variation).username_variation_no)

    def get_language(self):
        return self.cleaned_data.get('language', translation.get_language())

    class Meta(BaseUserCreationForm.Meta):
        fields = BaseUserCreationForm.Meta.fields + ['profile_colour']
        model = BaseUserCreationForm.Meta.model
        fieldsets = [
            ('user', {
                'fields': ['username_postfix', 'username', 'profile_colour'],
                'legend': 'Username',
                'classes': ['username'],
                'description': ''
            }),
            ('credentials', {
                'fields': ['password1', 'password2', 'security_question_1', 'security_answer_1', 'security_question_2', 'security_answer_2'],
                'legend': 'Credentials',
                'classes': ['user-cred'],
                'description': ''
            }),
        ]


class UserChangeForm(UserRegistrationForm):
    username = None
    username_postfix = None

    password1 = forms.CharField(label=_('new password'), widget=forms.PasswordInput, required=False, help_text=_("Specify a new password if you want to change it."))
    password2 = forms.CharField(label=_('confirm new password'), widget=forms.PasswordInput, required=False, help_text=_("Confirm your new password."))
    current_password = forms.CharField(label=_('current password'), widget=forms.PasswordInput, help_text=_("Enter your current password."))

    security_question_1 = forms.ModelChoiceField(label=_('Security question 1'), queryset=SecurityQuestionDataView.all(), required=False)
    security_question_2 = forms.ModelChoiceField(label=_('Security question 2'), queryset=SecurityQuestionDataView.all(), required=False)

    security_answer_1 = forms.CharField(label=_('Security answer 1'), max_length=255, required=False)
    security_answer_2 = forms.CharField(label=_('Security answer 2'), max_length=255, required=False)

    language = forms.ModelChoiceField(label=_('Language'), queryset=Language.objects.filter(status='act'))

    privacy_policy = None
    terms_of_use = None

    def clean_current_password(self):
        password = self.cleaned_data.get("current_password")
        if not self.instance.check_password(password):
            raise forms.ValidationError("Enter a valid password")
        return password

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)

        user.profile_colour = self.cleaned_data.get('profile_colour')

        question = self.get_security_question_1()
        answer = self.get_security_answer_1()
        question_2 = self.get_security_question_2()
        answer_2 = self.get_security_answer_2()

        user.language = self.get_language()

        if self.check_if_questions_set(question, answer, question_2, answer_2):
            user.security_question_1 = question
            user.security_answer_1 = make_password(answer)

            user.security_question_2 = question_2
            user.security_answer_2 = make_password(answer_2)

        user.save(force_update=True)

        return user

    def get_security_question_1(self):
        question = self.cleaned_data.get('security_question_1')
        return question.question if hasattr(question, 'question') and not question == u'' else None

    def get_security_answer_1(self):
        answer = self.cleaned_data.get('security_answer_1')
        return answer if not answer == u'' else None

    def get_security_question_2(self):
        question = self.cleaned_data.get('security_question_2')
        return question.question if hasattr(question, 'question') and not question == u'' else None

    def get_security_answer_2(self):
        answer = self.cleaned_data.get('security_answer_2')
        return answer if not answer == u'' else None

    def get_language(self):
        return self.cleaned_data.get('language', translation.get_language())

    def clean(self):
        question = self.get_security_question_1()
        answer = self.get_security_answer_1()
        question_2 = self.get_security_question_2()
        answer_2 = self.get_security_answer_2()

        if not self.check_both_questions_and_answers(question, answer, question_2, answer_2):
            raise forms.ValidationError("When resetting your security questions, both the answer and question must be given.")

        if not self.check_both_questions_are_set(question, answer, question_2, answer_2):
            raise forms.ValidationError("Both security questions must be given")

        return self.cleaned_data

    @classmethod
    def check_question_and_answer(cls, question, answer):
        """
        Both question and answer must be given, or none at all
        """
        if (question and not answer) or (answer and not question):
            return False

        return True

    @classmethod
    def check_both_questions_and_answers(cls, question, answer, question_2, answer_2):
        if not cls.check_question_and_answer(question, answer) or not cls.check_question_and_answer(question_2, answer_2):
            return False

        return True

    @classmethod
    def check_both_questions_are_set(cls, question, answer, question_2, answer_2):
        """
        Both questions and answers must be given, or none at all
        """
        if cls._is_set(question, answer) != cls._is_set(question_2, answer_2):
            return False

        return True

    @classmethod
    def _is_set(cls, question, answer):
        return True if question and answer else False

    @classmethod
    def check_if_questions_set(cls, question, answer, question_2, answer_2):
        if cls._is_set(question, answer) and cls._is_set(question_2, answer_2):
            return True

    class Meta(BaseUserCreationForm.Meta):
        fields = ['current_password', 'profile_colour']
        model = BaseUserCreationForm.Meta.model

        fieldsets = [
            ('user', {
                'fields': ['profile_colour', 'current_password', 'password1', 'password2'],
                'legend': '',
                'classes': ['user-details'],
                'description': ''
            }),
            ('user-extra', {
                'fields': ['security_question_1', 'security_answer_1', 'security_question_2', 'security_answer_2'],
                'legend': 'security questions',
                'classes': ['user-security'],
                'description': _('Reset your current security questions by setting new ones.')
            }),
        ]
        widgets = {
        }


class UsernameForm(forms.ModelForm):
    """
    An admin form to enable username generation

    Use cases:
        er kunnen maximaal 100 usernames ingevoerd worden door de admin
        een admin kan een username keuze verwijderen, dit verwijderd alle gegenereerde combinaties
        aan admin kan een username keuze aanmaken

        als de admin een nieuwe username aanmaakt dna worden alle mogelijke combinaties gegenereerd
        dit zodat je bij het maken van het user account een suggestie kunt doen voor een nog mogeiljke combinatie van username+id
        ook kun je zo gemakkelijker valideren of een username nog kan bestaan
    """

    def clean_active(self):
        active = self.cleaned_data.get('active', False)

        if active and UsernameDataView.active().count() >= 100:
            raise forms.ValidationError("You've exceeded the max number of 100 active usernames")

        return active

    def save(self, commit=True):
        username = super(UsernameForm, self).save(commit)

        username.save()  # For some reason this needs to be done in order to get a PK

        UsernameVariationDataView.generate(username)

        return username

    class Meta:
        model = Username
        exclude = []


class PWResetUsernameForm(forms.Form):
    username = forms.CharField(label=_("Your username"))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not UserDataView.username_exists(username):
            raise forms.ValidationError("That username does not exist.")

        return username


class PWResetFormQuestion(forms.Form):
    question = None
    answer = None
    user = None
    security_answer = forms.CharField(label=_('Answer'))

    def clean_security_answer(self):
        answer = self.cleaned_data.get('security_answer')
        if not self.user.check_security_answers(answer, self.answer):
            raise forms.ValidationError("That's an incorrect answer!")


class SetPasswordForm(BaseSetPasswordForm):
    user = None

    def __init__(self, *args, **kwargs):
        """
        Overload inheritance to avoid setting user via init
        """
        super(SetPasswordForm, self).__init__(self.user, *args, **kwargs)


class PasswordConfirmationForm(BetterForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordConfirmationForm, self).__init__(*args, **kwargs)

    current_password = forms.CharField(label=_('current password'), widget=forms.PasswordInput, help_text=_("Enter your current password."))

    def clean_current_password(self):
        password = self.cleaned_data.get("current_password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Enter a valid password")
        return password

    def save(self, request):
        logout(request)
        UserDataView.delete(self.user)
