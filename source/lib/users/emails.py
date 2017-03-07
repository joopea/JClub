from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from lib.emails.base_emails import BaseEmail
from django.utils.translation import ugettext_lazy as _


class PasswordResetMail(BaseEmail):
    template_name = 'emails/password_reset.html'

    def __init__(self, user, request, *args, **kwargs):

        self.to = [user.email]
        self.object = user

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        protocol = 'https' if request.is_secure() else 'http'

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        url = '{0}://{1}{2}'.format(protocol, domain, url)

        self.context_data = {
            'domain': domain,
            'site_name': site_name,
            'url': url,
        }

        self.subject = _("Password reset request for {0}".format(site_name))

        super(PasswordResetMail, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PasswordResetMail, self).get_context_data(**kwargs)
        context.update(self.context_data)
        return context

send_password_reset_mail = PasswordResetMail.as_callable()


class RegistrationConfirmationMail(BaseEmail):
    template_name = 'emails/registration_confirmation.html'

    def __init__(self, user, *args, **kwargs):

        self.to = [user.email]
        self.object = user
        self.subject = _("Thank you for registering")

        super(RegistrationConfirmationMail, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegistrationConfirmationMail, self).get_context_data(**kwargs)
        context.update(self.context_data)
        return context

send_registration_confirmation_mail = RegistrationConfirmationMail.as_callable()
