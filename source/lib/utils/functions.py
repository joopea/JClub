from django.core.urlresolvers import resolve, reverse
from django.utils.translation import override


def import_path(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def _get_current_view(request_path):
    current_view = resolve(request_path)

    func_name = current_view.url_name

    if current_view.namespace:
            func_name = ':'.join([current_view.namespace, func_name])

    return current_view, func_name


def _reverse(language_code, current_view, func_name):
    with override(language_code):
        return reverse(func_name, kwargs=current_view.kwargs)


def switch_language_url(language, request_path, fall_back='/'):
    current_view, func_name = _get_current_view(request_path)
    return _reverse(language, current_view, func_name)