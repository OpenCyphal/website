#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import os
import sys
import time
import datetime
from flask import Flask, g
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

app = Flask(__name__.split('.')[0])
app.config.from_object('config')

# Error tracking infrastructure
if not os.environ.get('DEBUG', ''):
    sentry_sdk.init(dsn="https://cf30bf083a464dcfb81e523979ead040@sentry.io/1384470",
                    integrations=[FlaskIntegration()])
else:
    print('WARNING: SENTRY NOT INITIALIZED', file=sys.stderr)

app.config['CURRENT_YEAR'] = datetime.datetime.now().year

from app import view


@app.before_request
def before_request():
    g.request_timestamp = time.time()
    g.get_time_since_request_ms = lambda: int((time.time() - g.request_timestamp) * 1000 + 1)
