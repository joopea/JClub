from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView


class GenericViewTestHandler(object):

    def __init__(self, url=None, form_data=None):
        self.url = url
        self.form_data = form_data

    def test_assert_page_status_code(self):
        self.assert_page_status_code(url=self.resolved_url, status_code=200)


class ListViewGenericTestView(GenericViewTestHandler):
    pass


class FormViewGenericTest(GenericViewTestHandler):

    def test_assert_status_code_200_after_form_submit(self):
        self.assert_form_submit_status_code(url=self.resolved_url, form_data=self.form_data, status_code=200)


class CreateViewGenericTest(FormViewGenericTest):
    pass


class UpdateViewGenericTest(FormViewGenericTest):
    pass


class DeleteViewGenericTest(FormViewGenericTest):
    pass


class GenericViewTestHandlerFactory(object):

    generic_view_test_handler_mapping = {
        CreateView: CreateViewGenericTest,
        UpdateView: UpdateViewGenericTest,
        DeleteView: DeleteViewGenericTest,
        ListView: ListViewGenericTestView,
    }

    @classmethod
    def get_generic_view_test_handler(cls, generic_view=None, url=None, form_data=None):
        url = reverse(url)
        return cls.generic_view_test_handler_mapping[generic_view](url=url, form_data=form_data)
