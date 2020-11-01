#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from .. import app
from ..model import devel_feed, forum_feed, adopters
from flask import render_template


FEED_LENGTH = 15


TITLE = 'UAVCAN - a lightweight protocol designed for reliable communication ' \
        'in aerospace and robotic applications over robust vehicular networks'


# noinspection PyBroadException
@app.route('/')
def _index():
    try:
        development_feed_entries = devel_feed.get(max_items=FEED_LENGTH)
    except Exception:
        development_feed_entries = None
        app.logger.exception('Devel feed error')

    try:
        forum_feed_entries = forum_feed.get(max_items=FEED_LENGTH)
    except Exception:
        forum_feed_entries = None
        app.logger.exception('Forum feed error')

    adopter_list = adopters.get_list()

    return render_template('home.html',
                           title=TITLE,
                           development_feed_entries=development_feed_entries,
                           forum_feed_entries=forum_feed_entries,
                           adopters=adopter_list)
