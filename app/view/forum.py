#
# Copyright (C) 2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from .. import app
from flask import redirect


_FORUM_URL = "https://forum.opencyphal.org"


@app.route("/forum/")
def _forum():
    return redirect(_FORUM_URL)
