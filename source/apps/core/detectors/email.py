import re
from django.utils.translation import ugettext_lazy as _

regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|[\s\.]at[\s\.])(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))


def get_emails(s):
    """Returns an iterator of matched emails found in string s."""
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
    return (email[0] for email in re.findall(regex, s) if not email[0].startswith('//'))


class WithEmailDetection(object):
    def __init__(self, *args, **kwargs):
        super(WithEmailDetection, self).__init__(*args, **kwargs)
        self.emails = []

    def clean(self, *args, **kwargs):
        cleaned_data = super(WithEmailDetection, self).clean(*args, **kwargs)
        message = cleaned_data.get('message', '') + cleaned_data.get('title', '')
        if message:
            emails = list(get_emails(message))
            self.emails = emails
        return cleaned_data

    def save(self, *args, **kwargs):
        instance = super(WithEmailDetection, self).save(*args, **kwargs)
        if len(self.emails):
            self.add_disapproval_reason('Possible email addresses found: {0}'.format(", ".join(self.emails)))  # Do not translate!
        return instance
