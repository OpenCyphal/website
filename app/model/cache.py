#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import time
import urllib.request
import threading
from . import expiring_storage
from .. import app


def get(url, background_update_interval, cache_expiration_timeout, headers=None):
    """
    Returns None if such URL is not (yet) cached.
    Cached entries will be removed after the specified period of inactivity.
    The timing parameters should not change between calls;
    otherwise, their actual values may vary unpredictably within the supplied ranges.
    """
    if background_update_interval >= cache_expiration_timeout:
        raise ValueError(
            "The background update interval must be lower than the data expiration timeout"
        )

    # First, decide if it is time to launch a background update yet.
    # Due to the race condition, we may accidentally start multiple updates concurrently, but this is fine.
    lock_key = "lock-" + url
    if not expiring_storage.read(lock_key):
        expiring_storage.write(
            lock_key, True, timeout=float(background_update_interval)
        )
        threading.Thread(
            target=lambda: _do_background_update(
                url, headers, cache_expiration_timeout
            ),
            daemon=False,
        ).start()

    return expiring_storage.read(url)


def _do_background_update(url, headers, cache_expiration_timeout):
    app.logger.info(
        "Initiating background update from %r with headers %r", url, headers
    )

    started_at = time.monotonic()
    r = urllib.request.Request(url, headers=headers or {})
    data = urllib.request.urlopen(r).read()

    expiring_storage.write(url, data, timeout=float(cache_expiration_timeout))

    app.logger.info(
        "Background update OK: saved %.1f KiB from %r in %.3f seconds",
        len(data) / 1024,
        url,
        time.monotonic() - started_at,
    )
