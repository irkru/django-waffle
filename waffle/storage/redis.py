from __future__ import unicode_literals, absolute_import

import hashlib

import redis

from waffle import KEY_PREFIX, REDIS
from waffle.storage.base import BaseStorage


class RedisStorage(BaseStorage):

    def __init__(self, *args, **kwargs):
        super(RedisStorage, self).__init__(*args, **kwargs)

        self.redis = redis.StrictRedis(**REDIS)
        remote_addr = self.request.META.get('REMOTE_ADDR', u'')
        user_agent = self.request.META.get('HTTP_USER_AGENT', u'')
        # Ignore non-ascii chars
        if not isinstance(user_agent, unicode):
            user_agent = user_agent.decode('utf-8', 'ignore')

        self.user_key = KEY_PREFIX % hashlib.sha1(
            u''.join([remote_addr, user_agent]).encode('utf-8')
        ).hexdigest()

    def __setitem__(self, key, value):
        return self.redis.hset(self.user_key, key, int(bool(value)))

    def __getitem__(self, key):
        value = self.redis.hget(self.user_key, key)
        if value is not None:
            return value == '1'

    def __contains__(self, key):
        return self.redis.hexists(self.user_key, key)
