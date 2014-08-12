# coding: utf-8

from waffle.tests.test_waffle import get
from waffle.tests.base import TestCase
from waffle.storage.redis import RedisStorage


class RedisStorageTest(TestCase):
    def test_non_unicode_chars_in_headers(self):
        request = get()

        request.META[u'HTTP_USER_AGENT'] = 'Не unicode строка'
        self.assertIsInstance(RedisStorage(request), RedisStorage)

        request.META[u'HTTP_USER_AGENT'] = u'Unicode строка'
        self.assertIsInstance(RedisStorage(request), RedisStorage)