from django.contrib.auth.models import AbstractBaseUser as AbstractDjangoUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from lib.users.managers import BaseUserManager


class UserExtra(models.Model):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class AbstractBaseUser(AbstractDjangoUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Password and username-field are required. Other fields are optional.

    You must determine the field which is used as username. This can be done by setting the constant
    USERNAME_FIELD to the desired attrib. Everything, including forms will follow automatically
    """

    USERNAME_FIELD = ''
    REQUIRED_FIELDS = []

    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = BaseUserManager()

    def __unicode__(self):
        return unicode(self.get_username())

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def set_username(self, username):
        return setattr(self, self.USERNAME_FIELD, username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.get_username()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.get_username()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class BaseUser(AbstractBaseUser, UserExtra):
    """
    Base user with email set as username field
    """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(_('e-mail'), unique=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True