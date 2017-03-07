from django.shortcuts import _get_queryset
from .exceptions import JsonNotFound


def get_object_or_json404(klass, *args, **kwargs):

    queryset = _get_queryset(klass)

    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise JsonNotFound()
