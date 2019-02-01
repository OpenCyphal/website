#!/usr/bin/env python3

import sys
import os

if sys.version_info[0] != 3:
    raise Exception('Invalid Python version')

sys.path.insert(0, os.path.dirname(__file__))
from app import app as application
