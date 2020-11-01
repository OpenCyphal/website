#
# Copyright (C) 2020 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from .. import app
from flask import render_template


TITLE = 'UAVCAN - a lightweight protocol designed for reliable communication ' \
        'in aerospace and robotic applications over robust vehicular networks'


@app.route('/conformant-products')
def conformant_products():

    return render_template('conformant-products.html',
                           title=TITLE)
