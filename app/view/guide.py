#
# Copyright (C) 2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import os
from flask import render_template, send_file, abort
from .. import app
from .home import TITLE


_GUIDE_DIRECTORY_PATH = os.path.join(app.root_path, '..', 'guide')


@app.route('/guide')
def guide():
    return render_template('guide.html',
                           title=TITLE)


@app.route('/guide/<path:file_name>')
def _guide_document(file_name):
    try:
        return send_file(os.path.join(_GUIDE_DIRECTORY_PATH, file_name))
    except FileNotFoundError:
        return abort(404)
