from django.conf import settings
from django.utils.module_loading import import_by_path


def default_storage(request):
    """
    Callable with the same interface as the storage classes.
    """

    return import_by_path(settings.WAFFLE_STORAGE)(request)
