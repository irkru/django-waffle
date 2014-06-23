from __future__ import unicode_literals

from django.conf import settings
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.contrib.messages import constants, utils


class BaseStorage(object):
    """
    This is the base backend for temporary message storage.

    This is not a complete class; to be a usable storage backend, it must be
    subclassed and the two methods ``_get`` and ``_store`` overridden.
    """

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseStorage, self).__init__(*args, **kwargs)

    def __contains__(self, key):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __getitem__(self, key):
        raise NotImplementedError()
