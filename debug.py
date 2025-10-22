#!/usr/bin/env python3

import sys
import logging
import os

os.environ["DEBUG"] = "1"

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
log_level = logging.DEBUG if "debug" in sys.argv else logging.INFO
logging.basicConfig(stream=sys.stderr, level=log_level, format=LOG_FORMAT)

sys.path.insert(0, os.path.dirname(__file__))

# noinspection PyUnresolvedReferences
from app import app as application

application.run(host="0.0.0.0", port=4000, debug=True)
