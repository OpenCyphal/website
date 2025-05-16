#
# Copyright (C) 2019 UAVCAN Development Team <info@zubax.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#
from urllib.parse import urljoin

from .. import app
from flask import redirect

_OPENCYPHAL_GH_PAGE = "https://opencyphal.github.io/"
_SPECIFICATION_FILE = "Cyphal_Specification.pdf"

@app.route('/specification/')
def _latest_specification():
    return redirect(urljoin(_OPENCYPHAL_GH_PAGE, f'specification/{_SPECIFICATION_FILE}'), code=301)
