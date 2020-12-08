#
# Copyright (C) 2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from .. import app
from flask import redirect


_LEGACY_URL = 'https://legacy.uavcan.org'


@app.route('/legacy/')
def _legacy():
    return redirect(_LEGACY_URL)
