from conductor import Conductor
from instruments.instrument import doublebass, piano, lofikit, synthpad
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
io = SocketIO()
io.init_app(app, cors_allowed_origins="*", async_mode="eventlet")


@app.route("/")
def index():
    return "Index Page API"


instruments = [piano, doublebass, lofikit, synthpad]

conductor = Conductor(app, io, instruments)
conductor.start()

if __name__ == "__main__":
    io.run(app, debug=True)
