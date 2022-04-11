#
# Copyright (C) 2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from .. import app
from flask import redirect


_GITHUB_URL = 'https://github.com/OpenCyphal'


@app.route('/github/')
def _github():
    return redirect(_GITHUB_URL)
