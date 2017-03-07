import importlib
from django.core.urlresolvers import reverse, resolve
from lib.testing.generic_tests.test_handlers import GenericViewTestHandlerFactory
from lib.testing.generic_tests.exceptions import NoGenericTestHandlerException


def run_generic_crud_tests(cls):
    """
    Class decorator that adds the tests for a generic view type (e.g listview, createview, etc)
    to the MRO of the decorated class.
    :param cls:
    :return:
    """
    added = False

    cls.resolved_url = reverse(cls.url, kwargs=cls.url_arguments)

    view_func = resolve(cls.resolved_url).func
    module = importlib.import_module(view_func.__module__)
    view = getattr(module, view_func.__name__)

    mro = view.mro()
    for definition in mro:
        if definition in GenericViewTestHandlerFactory.generic_view_test_handler_mapping:
            cls_to_add = GenericViewTestHandlerFactory.generic_view_test_handler_mapping[definition]
            cls.__bases__ += (cls_to_add, )
            added = True

    if not added:
        raise NoGenericTestHandlerException('No test handler found')

    return cls
