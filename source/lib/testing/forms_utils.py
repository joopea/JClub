from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.functional import lazy
from django.utils.importlib import import_module
from lib.testing.selenium.form_helpers import SeleniumFormTesthelper


class TestFile(object):
    """
    Responsible for handling an uploaded file to be used in tests, file will be initialized
    and its properties are available as instance properties.
    """

    name = None
    file = None
    location = None

    def __init__(self, file_name=None):

        file_location = settings.TEST_FILES_LOCATION + file_name

        try:
            uploaded_file = open(file_location, 'rb')
        except FileNotFoundError:
            raise FileNotFoundError(
                "Could not find {file_name} in {file_location}".format(
                    file_name=file_name,
                    file_location=file_location,
                ))

        self.file = SimpleUploadedFile(uploaded_file.name, uploaded_file.read())
        self.name = self.file.name
        self.location = uploaded_file.name


class FileNotFoundError(OSError):
    pass


def lazy_resolve(model=None, data=None, key=None):
    """
    lazy resolver for test scenario forms/scenarios,
    create the test scenario and returns the object instance or key value
    """

    def resolve_relation():
        return_value = None
        imported_model = load_testhelpers()[model]

        form_instance = imported_model.form(data=imported_model.test_data[data]).save()

        if key:
            return_value = getattr(form_instance, key)

        return return_value or form_instance

    # The Django lazy function only resolves if one of the following types is requested, extend if necessary.
    return lazy(resolve_relation, int, str, object)


def load_testhelpers():
    """
    :return: dictionary with all testhelpers classes from all the registered django apps
    with an test_helper file and the 'SeleniumFormTesthelper' class in the MRO
    """
    test_helpers = {}

    for app in settings.INSTALLED_APPS:
        try:
            module = import_module('.'.join((app, 'test_helper')))
            for member in dir(module):
                if SeleniumFormTesthelper in getattr(module, member).mro():
                    test_helpers[member] = getattr(module, member)
        except (ImportError, AttributeError):
            # Pass if there's no test helper file
            pass

    return test_helpers
