#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import json
import datetime
from .. import app
from . import cache


_FORUM_URL = "https://forum.opencyphal.org"
_3RD_PARTY_CATEGORY_ID = 18

_UPDATE_INTERVAL = 60
_CACHE_LIFETIME = 3600 * 24

_IMAGE_SIDE = 128


class Entry:
    def __init__(self, title, num_posts, url, image_url, timestamp, pinned):
        self.title = str(title)
        self.num_posts = int(num_posts)
        self.url = str(url)
        self.image_url = image_url
        self.timestamp = timestamp
        self.pinned = bool(pinned)

    @staticmethod
    def new(topic: dict, user_id_lookup: dict):
        image_url = topic.get("image_url")
        if not image_url:
            try:
                # Avatar lookup as a fall-back
                user = user_id_lookup[topic["posters"][0]["user_id"]]
                avatar_url_template = user["avatar_template"]
                image_url = avatar_url_template.replace("{size}", str(_IMAGE_SIDE))
            except KeyError:
                image_url = None

        if image_url and "://" not in image_url:
            # Some URLs may be full-formed, some may be relative; we have to unify
            image_url = _FORUM_URL + "/" + image_url

        return Entry(
            title=topic["title"],
            num_posts=topic["posts_count"],
            url=_FORUM_URL + "/t/" + str(topic["id"]),
            image_url=image_url,
            timestamp=datetime.datetime.strptime(topic["bumped_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            pinned=(topic.get("pinned") or topic.get("pinned_globally"))
            and topic.get("category_id") != _3RD_PARTY_CATEGORY_ID,
        )


def get(max_items):
    max_items = int(max_items)
    assert max_items > 0

    response = (
        cache.get(
            _FORUM_URL + "/latest.json",
            background_update_interval=_UPDATE_INTERVAL,
            cache_expiration_timeout=_CACHE_LIFETIME,
        )
        or b"{}"
    )
    data = json.loads(response.decode())
    if data:
        user_id_lookup = {u["id"]: u for u in data["users"]}
        entries = []
        for topic in data["topic_list"]["topics"]:
            # noinspection PyBroadException
            try:
                e = Entry.new(topic, user_id_lookup)
                if e:
                    entries.append(e)
            except Exception:
                app.logger.exception("Could not process entry")
                pass

        entries = sorted(entries, key=lambda x: x.timestamp, reverse=True)
        entries = sorted(entries, key=lambda x: x.pinned, reverse=True)
        return list(entries)[:max_items]
