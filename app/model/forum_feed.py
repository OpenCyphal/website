#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import json
import datetime
from .. import app
from . import cache


_FORUM_URL = 'https://forum.uavcan.org'

_UPDATE_INTERVAL = 60
_CACHE_LIFETIME = 3600 * 24


class Entry:
    def __init__(self, title, num_posts, url, timestamp):
        self.title = str(title)
        self.num_posts = int(num_posts)
        self.url = str(url)
        self.timestamp = timestamp

    @staticmethod
    def new(d: dict):
        return Entry(title=d['title'],
                     num_posts=d['posts_count'],
                     url=_FORUM_URL + '/t/' + str(d['id']),
                     timestamp=datetime.datetime.strptime(d['bumped_at'], '%Y-%m-%dT%H:%M:%S.%fZ'))


def get():
    response = cache.get(_FORUM_URL + '/latest.json',
                         background_update_interval=_UPDATE_INTERVAL,
                         cache_expiration_timeout=_CACHE_LIFETIME) or b'{}'
    data = json.loads(response.decode())
    if data:
        entries = []
        for topic in data['topic_list']['topics']:
            # noinspection PyBroadException
            try:
                e = Entry.new(topic)
                if e:
                    entries.append(e)
            except Exception:
                app.logger.exception('Could not process entry')
                pass

        return entries
