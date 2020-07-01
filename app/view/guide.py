#
# Copyright (C) 2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from .. import app
from flask import redirect


_GUIDE_URL = 'https://forum.uavcan.org/t/778'


@app.route('/guide/')
def _guide():
    return redirect(_GUIDE_URL)
