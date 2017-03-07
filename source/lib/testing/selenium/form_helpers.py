from selenium.common.exceptions import NoSuchElementException
from lib.testing.selenium.exceptions import FormUnknownFieldException, FormInputException
from lib.testing.selenium.input_handlers import SeleniumInputHandlerFactory


class SeleniumFormTesthelper(object):
    """
    Mixin that provides Selenium helper functions for handling forms
    """

    def get_field_input_handler(self, field_name):
        field = self.get_field(field_name=field_name)
        return SeleniumInputHandlerFactory.get_input_handler(
            widget_type=field.widget.__class__.__name__,
            selector=self.get_selector(field_name),
            selenium=self.selenium,
        )

    def get_field_value(self, field_name):
        field_handler = self.get_field_input_handler(field_name)
        return field_handler.get_value()

    def get_field_error(self, field_name):
        field = self.get_field_input_handler(field_name)
        return field.get_error()

    def get_form_error(self):
        form_error = None

        try:
            form_error = self.selenium.find_element_by_css_selector(css_selector='.errorlist').text
        except NoSuchElementException:
            # Return None if there's no error to report
            pass

        return form_error

    def _get_record(self, field_name):
        pass

    def submit(self):
        self.selenium.find_element_by_css_selector(css_selector='input[type="submit"]').click()


class DjangoFormTesthelper(object):
    """
    Mixin that provides is responsible for handling functionality related to Django forms
    """
    form = None

    def __init__(self):
        self.form = self.get_form(form=self.form)

    def get_form(self, form=None):
        form = form({})
        form.is_valid()
        return form

    def get_field(self, field_name):
        try:
            return self.form.fields[field_name]
        except KeyError:
            raise FormUnknownFieldException(
                "{form} has no field '{field_name}'".format(form=self.form.__class__, field_name=field_name))

    def get_fields(self):
        return self.form.fields

    def get_selector(self, field_name):
        return self.form[field_name].id_for_label


class SeleniumDjangoFormTesthelper(DjangoFormTesthelper, SeleniumFormTesthelper):
    """
    Concrete Baseclass for Django Form helper classes to extend from
    """

    default_validation_error = "Dit veld is verplicht."
    test_data = []

    def __init__(self, selenium=None):
        super(SeleniumDjangoFormTesthelper, self).__init__()
        self.selenium = selenium

    def field_fill(self, field_name, value):
        input_handler = self.get_field_input_handler(field_name)

        try:
            input_handler.fill(value=value)
        except NoSuchElementException:
            raise FormInputException("Could not find {name}".format(name=field_name))

    def form_fill(self, test_data=None):
        for field, value in self.test_data[test_data].iteritems():
            self.field_fill(field_name=field, value=value)

    def assert_field(self, field_name=None):
        try:
            field_exists = self.get_field_input_handler(field_name)
        except FormUnknownFieldException:
            field_exists = False

        return bool(field_exists)

    def assert_field_value_equals(self, field_name, value):
        return self.get_field_value(field_name) == value

    def assert_field_value_not(self, field_name, value):
        return self.get_field_value(field_name) != value

    def assert_form_error(self):
        return bool(self.get_form_error())

    def assert_form_error_equals(self, value=None):
        return self.get_form_error() == value

    def assert_field_error(self, field_name=None):
        return bool(self.get_field_error(field_name))

    def assert_field_error_equals(self, field_name, expected_error):
        return self.get_field_error(field_name) == expected_error

    def assert_form_no_errors(self, test_data):
        for field, value in self.test_data[test_data].iteritems():
            assert not self.assert_field_error(field_name=field)

        assert not self.assert_form_error()

    def assert_record_equals(self, record, fields):
        pass

    def assert_record_equals_not(self):
        pass

    def assert_record_has_field(self):
        pass

    def assert_record_has_record(self):
        pass
