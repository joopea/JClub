import settings

from emailtools import HTMLEmail


class BaseEmail(HTMLEmail):
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [settings.CUSTOMER_EMAIL]
    template_name = 'emails/base.html'

    subject = ''
    cc = None
    bcc = None
    body = None
    attachments = None
    headers = None
    object = None
    context_data = None

    def __init__(self, recipient_list=None, context_object=None, context_data=None, *args, **kwargs):
        self.to = recipient_list or self.to
        self.object = context_object or self.object
        self.context_data = context_data or self.context_data or {}

        super(BaseEmail, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseEmail, self).get_context_data(**self.context_data)
        context.update({'object': self.object})
        return context


class TestEmail(BaseEmail):
    subject = 'TEST E-MAIL'
    template_name = 'emails/test_email.jinja.html'

send_test_email = TestEmail.as_callable()

