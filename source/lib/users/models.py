from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.users.base_models import BaseUser


class User(BaseUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(_('e-mail'), unique=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
