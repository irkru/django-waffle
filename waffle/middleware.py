from __future__ import unicode_literals

from django.utils.encoding import smart_str

from waffle.utils import get_setting
from waffle.storage import default_storage

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object  # fallback for Django < 1.10


class WaffleMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        secure = get_setting('SECURE')
        max_age = get_setting('MAX_AGE')

        if hasattr(request, 'waffles'):
            storage = default_storage(request)
            for k in request.waffles:
                name = smart_str(get_setting('COOKIE') % k)
                active, rollout = request.waffles[k]
                if rollout and not active:
                    # "Inactive" is a session cookie during rollout mode.
                    age = None
                else:
                    age = max_age
                storage[name] = active

        if hasattr(request, 'waffle_tests'):
            for k in request.waffle_tests:
                name = smart_str(get_setting('TEST_COOKIE') % k)
                value = request.waffle_tests[k]
                # TODO: support storage
                response.set_cookie(name, value=value)

        return response
