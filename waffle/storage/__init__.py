from django.conf import settings

from django.utils.module_loading import import_string


def default_storage(request):
    """
    Callable with the same interface as the storage classes.
    """

    return import_string(settings.WAFFLE_STORAGE)(request)
