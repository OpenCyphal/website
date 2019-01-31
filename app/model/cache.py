#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import os
import time
import urllib.request
from . import expiring_storage
from .. import app


_DATA_EXPIRATION_TIMEOUT = 3600 * 24 * 7        # Should be very long
_UPDATE_INTERVAL = 300.0                        # Should be between one minute and a half of the expiration timeout


def get(url, headers=None):
    """
    Returns None if such URL is not (yet) cached.
    Cached entries will be removed after some (long) period of inactivity.
    """
    # First, decide if it is time to launch a background update yet.
    # Due to the race condition, we may accidentally start multiple updates concurrently, but this is fine.
    lock_key = 'lock-' + url
    if not expiring_storage.read(lock_key):
        expiring_storage.write(lock_key, True, timeout=_UPDATE_INTERVAL)
        if os.fork() == 0:
            _do_background_update(url, headers)

    return expiring_storage.read(url)


def _do_background_update(url, headers):
    app.logger.info('Initiating background update from %r with headers %r', url, headers)

    started_at = time.monotonic()
    r = urllib.request.Request(url, headers=headers or {})
    data = urllib.request.urlopen(r).read()
    app.logger.info('Loaded %.1f KiB from %r in %.3f seconds',
                    len(data) / 1024,
                    url,
                    time.monotonic() - started_at)

    expiring_storage.write(url, data, timeout=_DATA_EXPIRATION_TIMEOUT)
