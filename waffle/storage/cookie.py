from __future__ import unicode_literals

from waffle import KEY_PREFIX
from waffle.storage.base import BaseStorage


class CookieStorage(BaseStorage):
    # TODO: support cookies max age

    def __setitem__(self, key, value):
        name = KEY_PREFIX % key

        self.request.COOKIES[name] = 'True'

    def __getitem__(self, key):
        name = KEY_PREFIX % key

        if name in self.request.COOKIES:
            return self.request.COOKIES.get(name) == 'True'

    def __contains__(self, key):
        name = KEY_PREFIX % key

        return name in self.request.COOKIES
