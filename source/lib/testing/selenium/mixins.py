from django.contrib.auth.models import User


class AuthenticatedSeleniumTestCaseMixin(object):
    """
    This mixin provides functionality for creating roles and authenticating the Selenium session with the specified role
    """
    role = 'guest'
    auth_url = '/auth/inloggen/'

    AUTH_ROLES = {
        'admin': {
            'username': 'admin@getlogic.nl',
            'password': 'asdasd',
            'first_name': 'Ad',
            'last_name': 'Min',
            'is_superuser': True,
            'gender': 'm',
        },
        'user': {
            'username': 'test@user.com',
            'password': 'asdasd'
        },
        'guest': {
            'username': None,
            'password': None
        },
    }

    def setUp(self):
        super(AuthenticatedSeleniumTestCaseMixin, self).setUp()
        self.login(selenium=self.selenium)

    def login(self, selenium=None):
        user_data = self.AUTH_ROLES.get(self.role)
        if user_data['username'] is not None:
            self.user = User.objects.create_user(**user_data)

            selenium.get('%s%s' % (self.live_server_url, self.auth_url))
            selenium.find_element_by_id("id_username").send_keys(user_data['username'])
            selenium.find_element_by_id("id_password").send_keys(user_data['password'])

            self.click_through_to_new_page(css_selector="input.btn-primary")