import os
import threading

from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return "Bot ishlab turibdi ✅"


def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


def start_keepalive():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
