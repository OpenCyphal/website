#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import sys
import time
import datetime
from flask import Flask, g
from raven.contrib.flask import Sentry

app = Flask(__name__.split('.')[0])
app.config.from_object('config')

# Error tracking infrastructure
# if not app.config.get('DEBUG', False):
#     sentry = Sentry(app,
#                     dsn='https://ec37fc78d7144ee39e3a31f53ede70da:42da6bdb53fe4884b8540b46d23e8640@sentry.io/187341',
#                     logging=True,
#                     level=logging.ERROR)
# else:
#     print('WARNING: SENTRY NOT INITIALIZED', file=sys.stderr)
#     sentry = None

app.config['CURRENT_YEAR'] = datetime.datetime.now().year


from app import view


@app.before_request
def before_request():
    g.request_timestamp = time.time()
    g.get_time_since_request_ms = lambda: int((time.time() - g.request_timestamp) * 1000 + 1)
