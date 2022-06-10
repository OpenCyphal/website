from .. import app
from flask import redirect


_CHAT_URL = r'https://matrix.to/#/%23opencyphal:matrix.org'


@app.route('/chat/')
def _chat():
    return redirect(_CHAT_URL)
