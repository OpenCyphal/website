#
# Copyright (C) 2019-2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from ..model.adopters import get_logo_file_path
from .. import app
from flask import send_file, abort


@app.route('/adopters/logo/<path:logo_file_name>')
def _adopters_logo(logo_file_name):
    try:
        return send_file(get_logo_file_path(logo_file_name))
    except FileNotFoundError:
        return abort(404)
