from django.contrib.auth.models import UserManager
from django.utils import timezone


class BaseUserManager(UserManager):

    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, password and kwargs.

        Note that the actual username field is defined on the model, meaning "username" as param is ambiguous.

        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_username(username)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def _get_username(self, **kwargs):
        """
        Get username from kwargs and pop it from.
        """
        username = kwargs.get(self.model.USERNAME_FIELD, None)
        if username:
            del kwargs[self.model.USERNAME_FIELD]
        return username, kwargs

    def create_user(self, password, **kwargs):
        username, kwargs = self._get_username(**kwargs)
        return self._create_user(username, password, False, False, **kwargs)

    def create_superuser(self, password, **kwargs):
        username, kwargs = self._get_username(**kwargs)
        return self._create_user(username, password, True, True, **kwargs)
