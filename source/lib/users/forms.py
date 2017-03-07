from django import forms
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.utils.translation import ugettext_lazy as _, override
from form_utils.forms import BetterModelForm
from .data_views import UserDataView
from lib.users.emails import send_password_reset_mail, send_registration_confirmation_mail


class BaseLoginForm(AuthenticationForm):
    pass


class BaseUserCreationForm(BetterModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    send_mail = True

    error_messages = {
        'duplicate_username': _("This user already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()  # Get configured user model
        # add fields according to settings
        fieldsets = [
            ('user', {
                'fields': [model.USERNAME_FIELD, 'password1', 'password2'] + model.REQUIRED_FIELDS,
                'legend': '',
                'classes': ['user-details'],
                'description': ''
            }),
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'], code="password_mismatch")
        return password2

    def clean(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        # Do keep in mind this could be a security issue, because it enables the guessing of usernames
        username = self.get_username()

        if username and UserDataView.username_exists(username):
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )

    def get_username_field(self):
        model = self.Meta.model
        return model.USERNAME_FIELD

    def get_username(self):
        username_field = self.get_username_field()
        return self.cleaned_data.get(username_field)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(BaseUserCreationForm, self).save(commit=False)

        password = self.cleaned_data["password1"]
        if password:  # Set password formfield required to true or false, to enable inheritance
            user.set_password(password)

        if commit:
            user.save()

        if self.send_mail:
            self.send_mail(user)

        return user

    def authenticate_and_login(self, request):
        """
        Do login after registration. Keep in mind this function can only be called when the form is valid.
        """
        if not self.is_valid():
            raise Exception("This function should nog be called before form is valid")

        username = self.get_username()
        password = self.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        request.session.cycle_key()
        login(request, user)

    @classmethod
    def send_mail(cls, user):
        pass


class BaseUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_("The password can be changed via <a href=\"password/\">this form.</a>")
    )

    class Meta:
        model = get_user_model()
        exclude = []

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get("password", '')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, request):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        active_users = UserDataView.active_users(email)

    @classmethod
    def send_password_reset_mail(cls, user, request):
        pass


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user
