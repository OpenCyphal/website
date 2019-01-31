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
    def __init__(self, text, timestamp):
        self.text = str(text)
        self.timestamp = timestamp

    @staticmethod
    def new(d: dict):
        timestamp = datetime.datetime.strptime(d['bumped_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

        text = '%s (%d posts)' % (
            _render_url(d['title'], FORUM_URL + '/t/' + str(d['id'])),
            d['posts_count'],
        )

        return Entry(text=text, timestamp=timestamp)


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
