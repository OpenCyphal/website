#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import json
import datetime
from .. import app
from . import cache


class Entry:
    def __init__(self, text, timestamp):
        self.text = str(text)
        self.timestamp = timestamp

    @staticmethod
    def new(d: dict):
        if d['type'] == 'WatchEvent':
            text = ' '.join([
                _render_url(d['actor']['login'], d['actor']['url']),
                'starred',
                _render_url(d['repo']['name'], d['repo']['url']),
            ])
            timestamp = _strptime(d['created_at'])

        elif d['type'] == 'PullRequestEvent' and d['payload']['action'] in ('opened', 'closed', 'reopened'):
            text = ' '.join([
                _render_url(d['actor']['login'], d['actor']['url']),
                d['payload']['action'],
                'a pull request',
                '&ldquo;' +
                _render_url(d['payload']['pull_request']['title'], d['payload']['pull_request']['html_url']) +
                '&rdquo;',
                'at',
                _render_url(d['repo']['name'], d['repo']['url']),
            ])
            timestamp = _strptime(d['payload']['pull_request']['created_at'])

        elif d['type'] == 'IssuesEvent' and d['payload']['action'] in ('opened', 'closed', 'reopened'):
            text = ' '.join([
                _render_url(d['actor']['login'], d['actor']['url']),
                d['payload']['action'],
                'an issue',
                '&ldquo;' +
                _render_url(d['payload']['issue']['title'], d['payload']['issue']['html_url']) +
                '&rdquo;',
                'at',
                _render_url(d['repo']['name'], d['repo']['url']),
            ])
            timestamp = _strptime(d['payload']['issue']['created_at'])

        elif d['type'] == 'ForkEvent':
            text = ' '.join([
                _render_url(d['actor']['login'], d['actor']['url']),
                'forked',
                _render_url(d['repo']['name'], d['repo']['url']),
            ])
            timestamp = _strptime(d['payload']['forkee']['created_at'])

        elif d['type'] == 'PushEvent':
            text = ' '.join([
                _render_url(d['actor']['login'], d['actor']['url']),
                'pushed',
                str(len(d['payload']['commits'])),
                'commits to',
                _render_url(d['repo']['name'], d['repo']['url']),
            ])
            timestamp = _strptime(d['created_at'])

        elif d['type'] == 'IssueCommentEvent' and d['payload']['action'] in ('created', ):
            text = ' '.join([
                _render_url(d['actor']['login'], d['actor']['url']),
                'commented on',
                '&ldquo;' +
                _render_url(d['payload']['issue']['title'], d['payload']['issue']['html_url']) +
                '&rdquo;',
                'at',
                _render_url(d['repo']['name'], d['repo']['url']),
            ])
            timestamp = _strptime(d['payload']['issue']['created_at'])

        else:
            return

        return Entry(text=text, timestamp=timestamp)


def get():
    response = cache.get('https://api.github.com/orgs/UAVCAN/events',
                         headers={'Accept': 'application/vnd.github.v3+json'}) or b'[]'
    data = json.loads(response.decode())
    if data:
        entries = []
        for event in data:
            # noinspection PyBroadException
            try:
                e = Entry.new(event)
                if e:
                    entries.append(e)
            except Exception:
                app.logger.exception('Could not process event entry')

        return entries


def _render_url(text: str, target: str) -> str:
    target = target.replace('api.', '').replace('/repos/', '/').replace('/users/', '/')
    return '<a href="%s">%s</a>' % (target, text)


def _strptime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
