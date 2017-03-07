from django.contrib import admin
from django.contrib.auth import get_user_model

from lib.users.base_admin import BaseUserAdmin
from lib.users.mixins import AsSULoginMixin

UserModel = get_user_model()


class UserAdmin(AsSULoginMixin, BaseUserAdmin):
    pass

admin.site.register(UserModel, UserAdmin)
