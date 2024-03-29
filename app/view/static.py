#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import os
import fnmatch
from .. import app
from flask import send_from_directory, send_file, abort, redirect, render_template, request


# These are used to keep old links posted around the web functional.
# The wildcards are not case-sensitive.
# First match wins.
_COMPATIBILITY_REDIRECT_WILDCARDS = {
    '*hardware_design_recommendations*':
        'https://forum.opencyphal.org/t/removal-of-the-physical-layer-specification/895',
    '*specification*':      '/specification',  # Old website, also non-existent PDF versions.
    '/implementations*':    '/',
    '/contact*':            '/',
    '/uavcan*':             '/',
    '/gui_tool*':           'https://github.com/OpenCyphal/yakut',
    '/example*':            'https://github.com/OpenCyphal/demos',
}


@app.errorhandler(404)
def _not_found(_error):
    for wc, target in _COMPATIBILITY_REDIRECT_WILDCARDS.items():
        if fnmatch.fnmatch(request.path.lower(), wc.lower()):
            app.logger.info('Compatibility redirect: %r --> %r', request.path, target)
            return redirect(target, code=301)  # Moved permanently

    return render_template('http_error.html', error_description='File not found (404)'), 404


@app.route('/static/<path:p>')
def _static(p: str):
    path = os.path.join(app.root_path, 'static', p)
    if not os.path.exists(path):
        abort(404)

    return send_file(p)


@app.route('/favicon.ico')
def _favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'favicon.ico',
                               mimetype='image/x-icon')


@app.route('/favicon-152.png')
def _favicon_152():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'favicon-152.png',
                               mimetype='image/png')


@app.route('/favicon-192.png')
def _favicon_192():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'favicon-192.png',
                               mimetype='image/png')
