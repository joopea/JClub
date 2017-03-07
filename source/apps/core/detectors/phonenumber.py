import re
from django.utils.translation import ugettext_lazy as _

phonePattern = re.compile(
    r'''
    (            # don't match beginning of string, number can start anywhere
    (
    (\d{3})     # area code is 3 digits (e.g. '800')
    [\s\-]*         # optional separator is any number of non-digits
    (\d{3})     # trunk is 3 digits (e.g. '555')
    [\s\-]*         # optional separator
    (\d{1,4})     # rest of number is 4 digits (e.g. '1212')
    [\s\-]*         # optional separator
    (\d*)       # extension is optional and can be any number of digits
    )|(
    \d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d*      # 7 or more digits separated by optional whitespace
    )
    )
    ''', re.VERBOSE)


def get_phonenumbers(s):
    return (phone[0] for phone in re.findall(phonePattern, s) if len(phone[0]) <= 15)


class WithPhonenumberDetection(object):
    def __init__(self, *args, **kwargs):
        super(WithPhonenumberDetection, self).__init__(*args, **kwargs)
        self.phone_numbers = []

    def clean(self, *args, **kwargs):
        cleaned_data = super(WithPhonenumberDetection, self).clean(*args, **kwargs)
        message = cleaned_data.get('message', '') + cleaned_data.get('title', '')
        if message:
            phone_numbers = list(get_phonenumbers(message))
            self.phone_numbers = phone_numbers
        return cleaned_data

    def save(self, *args, **kwargs):
        instance = super(WithPhonenumberDetection, self).save(*args, **kwargs)
        if len(self.phone_numbers):
            self.add_disapproval_reason('Possible phone numbers found: {0}'.format(", ".join(self.phone_numbers)))  # Do not tranlate!
        return instance
