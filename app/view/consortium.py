#
# Copyright (C) 2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import os
from flask import render_template, send_file, abort
from .. import app
from .home import TITLE
from ..model import adopters


_CONSORTIUM_DIRECTORY_PATH = os.path.join(app.root_path, '..', 'consortium')


@app.route('/consortium')
def consortium():
    return render_template('consortium.html',
                           title=TITLE,
                           adopters=adopters.get_adopters())


@app.route('/consortium/<path:file_name>')
def _consortium_document(file_name):
    try:
        return send_file(os.path.join(_CONSORTIUM_DIRECTORY_PATH, file_name))
    except FileNotFoundError:
        return abort(404)
