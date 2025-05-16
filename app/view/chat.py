from .. import app
from flask import redirect


_CHAT_URI = "https://forum.opencyphal.org/chat"


@app.route('/chat/')
def _chat():
    return redirect(_CHAT_URI)
