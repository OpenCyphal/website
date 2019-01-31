#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from .. import app
from ..model import devel_feed, forum_feed
from flask import render_template


FEED_LENGTH = 15


TITLE = 'UAVCAN - a lightweight protocol designed for reliable communication ' \
        'in aerospace and robotic applications over robust vehicular networks'


@app.route('/')
def _index():
    try:
        development_feed_entries = _crop_feed(devel_feed.get())
    except Exception:
        development_feed_entries = None
        app.logger.exception('Devel feed error')

    try:
        forum_feed_entries = _crop_feed(forum_feed.get())
    except Exception:
        forum_feed_entries = None
        app.logger.exception('Forum feed error')

    return render_template('index.html',
                           title=TITLE,
                           development_feed_entries=development_feed_entries,
                           forum_feed_entries=forum_feed_entries)


def _crop_feed(f):
    return list(sorted(f or [], key=lambda x: x.timestamp, reverse=True))[:FEED_LENGTH]
