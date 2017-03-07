from django.contrib.auth import get_user_model
from lib.data_views.data_views import ModelDataView
from lib.data_views.exceptions import RecordDoesNotExist


class UserDataView(ModelDataView):

    @classmethod
    def get_model(cls):
        """
        Overriding get model to get_user_model.
        """
        return get_user_model()

    @classmethod
    def by_id(cls, user_id):
        return cls.get_or_404(id=user_id)

    @classmethod
    def username_exists(cls, username):
        """
        Check whether the username exists, based on the model configured username attr
        """
        kwargs = {
            cls.get_model().USERNAME_FIELD: username
        }

        try:
            cls.get(**kwargs)
            # If exists then return True
            return True
        except RecordDoesNotExist:
            return False

    @classmethod
    def active_users(cls, email):
        return cls.list(email__iexact=email, is_active=True)
