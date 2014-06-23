from django.conf import settings
from django.utils.encoding import smart_str

from waffle import COOKIE_NAME, TEST_COOKIE_NAME, default_storage


class WaffleMiddleware(object):
    def process_response(self, request, response):
        secure = getattr(settings, 'WAFFLE_SECURE', False)
        max_age = getattr(settings, 'WAFFLE_MAX_AGE', 2592000)  # 1 month

        if hasattr(request, 'waffles'):
            storage = default_storage(request)
            for k in request.waffles:
                name = smart_str(COOKIE_NAME % k)
                active, rollout = request.waffles[k]
                if rollout and not active:
                    # "Inactive" is a session cookie during rollout mode.
                    age = None
                else:
                    age = max_age
                storage[name] = active

        if hasattr(request, 'waffle_tests'):
            for k in request.waffle_tests:
                name = smart_str(TEST_COOKIE_NAME % k)
                value = request.waffle_tests[k]
                # TODO: support storage
                response.set_cookie(name, value=value)

        return response
