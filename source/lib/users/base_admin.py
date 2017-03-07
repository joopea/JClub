from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from lib.users.forms import BaseUserChangeForm, BaseUserCreationForm
from django.utils.translation import ugettext_lazy as _

UserModel = get_user_model()


class BaseUserAdmin(UserAdmin):
    """
    Base admin for the BaseUser model (see models.py)
    """
    # The forms to add and change user instances
    username_field = UserModel.USERNAME_FIELD

    form = BaseUserChangeForm
    add_form = BaseUserCreationForm

    list_display = (username_field, 'first_name', 'last_name', 'is_staff', 'is_superuser', )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {
            'fields': (
                username_field,
                'password'
            )}),
        (_('Personal data'), {
            'fields': (
                'first_name',
                'last_name',
            )}),
        ('Authorisation', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                'last_login',
                'date_joined'
            )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',),
            'fields': (
                username_field,
                'password1',
                'password2',
            )}),
    )
    search_fields = (username_field, 'first_name', 'last_name')
    ordering = ('date_joined', )