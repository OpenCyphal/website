#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from cachelib import FileSystemCache
from .. import app

_cache = FileSystemCache("/tmp/" + app.root_path)


def read(key):
    """
    Atomic cache read.
    If the entry does not exist, will return None.
    """
    return _cache.get(key)


def write(key, value, timeout=None):
    """
    Atomic cache write.
    If the timeout is not set, the entry will never expire.
    """
    _cache.set(key, value, timeout=timeout)
