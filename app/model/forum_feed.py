#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import json
import datetime
from .. import app
from . import cache


FORUM_URL = 'https://forum.uavcan.org'


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
                     url=FORUM_URL + '/t/' + str(d['id']),
                     timestamp=datetime.datetime.strptime(d['bumped_at'], '%Y-%m-%dT%H:%M:%S.%fZ'))


def get():
    response = cache.get(FORUM_URL + '/latest.json') or b'{}'
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


def _render_url(text: str, target: str) -> str:
    return '<a href="%s">%s</a>' % (target, text)
