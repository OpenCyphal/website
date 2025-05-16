# Copyright (C) OpenCyphal <maintainers@opencyphal.com>.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>

from flask import redirect
from .. import app

_SPECIFICATION_URI = "https://opencyphal.github.io/specification/Cyphal_Specification.pdf"


@app.route("/specification/", defaults={"subpath": ""})
@app.route("/specification/<path:subpath>")
def _latest_specification(subpath: str):
    _ = subpath
    return redirect(_SPECIFICATION_URI, code=301)
