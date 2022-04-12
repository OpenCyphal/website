#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import os
import re
import glob
from .. import app
from flask import send_file, redirect, abort


_SPECIFICATION_DIRECTORY_PATH = os.path.join(app.root_path, '..', 'specification')

_CYPHAL_SPECIFICATION_GLOB = 'Cyphal_Specification*.pdf'

@app.route('/specification/')
def _latest_specification():
    entries = list(glob.glob(os.path.join(_SPECIFICATION_DIRECTORY_PATH, _CYPHAL_SPECIFICATION_GLOB)))
    entries.sort(key=lambda t: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', t)])   # Natural sorting
    newest_file = os.path.basename(entries[-1])
    app.logger.info('Sorted specifications: %r, newest: %r', entries, newest_file)
    return redirect('/specification/' + newest_file)


@app.route('/specification/<path:file_name>')
def _particular_specification(file_name):
    try:
        return send_file(os.path.join(_SPECIFICATION_DIRECTORY_PATH, file_name),
                         mimetype='application/pdf')
    except FileNotFoundError:
        return abort(404)
