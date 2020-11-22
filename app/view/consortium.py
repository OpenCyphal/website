#
# Copyright (C) 2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from .. import app
from flask import render_template
from .home import TITLE


@app.route('/consortium')
def consortium():
    return render_template('consortium.html',
                           title=TITLE)
