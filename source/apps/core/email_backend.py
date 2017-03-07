from email.Utils import parseaddr
import re

from django.conf import settings
from django.utils.module_loading import import_by_path


# unerlying backend
klass = import_by_path(settings.EMAIL_BACKEND_BASE)

if settings.EMAIL_USE_WHITELIST:
    class WhitelistEmailBackend(klass):
        """ E-mail backend that filters mail based on the e-mail address. """

        def send_messages(self, email_messages):
            """ Discards mails without white-listed recipients. """
            filtered = []
            for email_message in email_messages:
                email_message.to = self.filter_addresses(email_message.to)
                email_message.cc = self.filter_addresses(email_message.cc)
                email_message.bcc = self.filter_addresses(email_message.bcc)
                if email_message.recipients():
                    filtered.append(email_message)

            return super(WhitelistEmailBackend, self).send_messages(filtered)

        def filter_addresses(self, email_addresses):
            """ Returns adresses matching white-list patterns. """
            allowed = []
            for email in email_addresses:
                name, address = parseaddr(email)
                for check in settings.EMAIL_FILTER_WHITELIST:
                    pattern = re.compile(check)

                    if pattern.match(address):
                        allowed.append(email)
                        break
            return allowed
else:
    # skip filtering entirely
    WhitelistEmailBackend = klass
